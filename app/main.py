from fastapi import FastAPI
from app.api import auth

app = FastAPI(title="SoundSphere API")

app.include_router(auth.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}