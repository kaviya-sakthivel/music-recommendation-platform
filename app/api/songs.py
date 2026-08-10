from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Song
from app.schemas.schemas import SongOut, SongCreate
from app.seed_songs import build_song_objects
from typing import List

router = APIRouter(prefix="/api/songs", tags=["songs"])


@router.get("/", response_model=List[SongOut])
def get_songs(db: Session = Depends(get_db)):
    return db.query(Song).all()


@router.post("/", response_model=SongOut)
def create_song(song: SongCreate, db: Session = Depends(get_db)):
    new_song = Song(**song.dict())
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song


@router.post("/seed")
def seed_songs(db: Session = Depends(get_db)):
    existing = db.query(Song).count()
    if existing > 0:
        db.query(Song).delete()
        db.commit()

    song_dicts = build_song_objects()
    song_objects = [Song(**s) for s in song_dicts]
    db.add_all(song_objects)
    db.commit()
    return {"message": "Songs seeded", "count": len(song_objects)}