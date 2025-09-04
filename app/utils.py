import os
from datetime import datetime, timedelta
from jose import jwt

STREAM_SECRET = os.getenv("SECRET_KEY", "dev-secret-change-me")   # reuse
ALGO = "HS256"
STREAM_LINK_EXPIRE_MINUTES = int(os.getenv("STREAM_LINK_EXPIRE_MINUTES", "10"))

def create_stream_token(media_id: int) -> str:
    exp = datetime.utcnow() + timedelta(minutes=STREAM_LINK_EXPIRE_MINUTES)
    payload = {"mid": media_id, "exp": exp}
    return jwt.encode(payload, STREAM_SECRET, algorithm=ALGO)

def decode_stream_token(token: str) -> int:
    data = jwt.decode(token, STREAM_SECRET, algorithms=[ALGO])
    return int(data["mid"])
