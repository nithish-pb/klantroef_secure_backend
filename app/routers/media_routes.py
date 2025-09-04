from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import MediaAsset, MediaViewLog
from ..schemas import MediaCreate, MediaOut
from ..security import get_current_user
from ..utils import create_stream_token, decode_stream_token
from sqlalchemy import func
from ..schemas import MediaAnalyticsOut


router = APIRouter(prefix="/media", tags=["media"])

# Create media (authenticated)
@router.post("", response_model=MediaOut)
def add_media(payload: MediaCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    media = MediaAsset(title=payload.title, type=payload.type, file_url=payload.file_url)
    db.add(media)
    db.commit()
    db.refresh(media)
    return media

# Generate secure 10-min stream URL (no auth requirement in spec)
@router.get("/{media_id}/stream-url")
def get_stream_url(media_id: int):
    token = create_stream_token(media_id)
    # This URL hits our optional /media/stream endpoint which validates the token
    return {"secure_url": f"/media/stream?token={token}"}

# (Optional) Validate token and "serve" stream (here we just confirm + log)
@router.get("/stream")
def stream_media(token: str, request: Request, db: Session = Depends(get_db)):
    try:
        media_id = decode_stream_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired link")

    # Log the view with client IP
    client_ip = request.client.host if request.client else "unknown"
    log = MediaViewLog(media_id=media_id, viewed_by_ip=client_ip)
    db.add(log)
    db.commit()
    # In a real app you would redirect/proxy to the actual file_url.
    return {"message": "Valid stream link", "media_id": media_id, "viewer_ip": client_ip}


# Log a view (authenticated)
@router.post("/{media_id}/view")
def log_view(media_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    media = db.query(MediaAsset).filter(MediaAsset.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    client_ip = request.client.host if request.client else "unknown"
    log = MediaViewLog(media_id=media_id, viewed_by_ip=client_ip)
    db.add(log)
    db.commit()
    return {"message": "View logged", "media_id": media_id, "viewer_ip": client_ip}


# Get analytics (authenticated)
@router.get("/{media_id}/analytics", response_model=MediaAnalyticsOut)
def get_analytics(media_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    media = db.query(MediaAsset).filter(MediaAsset.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    # Total views
    total_views = db.query(func.count(MediaViewLog.id)).filter(MediaViewLog.media_id == media_id).scalar()

    # Unique IPs
    unique_ips = db.query(func.count(func.distinct(MediaViewLog.viewed_by_ip))).filter(MediaViewLog.media_id == media_id).scalar()

    # Views per day
    rows = (
        db.query(func.date(MediaViewLog.timestamp), func.count(MediaViewLog.id))
        .filter(MediaViewLog.media_id == media_id)
        .group_by(func.date(MediaViewLog.timestamp))
        .all()
    )
    views_per_day = {str(date): count for date, count in rows}

    return MediaAnalyticsOut(
        total_views=total_views,
        unique_ips=unique_ips,
        views_per_day=views_per_day
    )
