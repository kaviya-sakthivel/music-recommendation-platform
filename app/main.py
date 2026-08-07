from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth
from app.core.database import Base, engine
from app.models import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SoundSphere API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}