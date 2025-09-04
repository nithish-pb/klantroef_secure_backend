from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth_routes, media_routes

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Klantroef Secure Backend")

# Basic CORS (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(media_routes.router)

@app.get("/")
def root():
    return {"status": "ok"}
