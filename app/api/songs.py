from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Song
from app.schemas.schemas import SongOut, SongCreate
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
        return {"message": "Songs already exist", "count": existing}

    sample_songs = [
        Song(title="Blinding Lights", artist="The Weeknd", genre="Pop", duration=200),
        Song(title="Levitating", artist="Dua Lipa", genre="Pop", duration=203),
        Song(title="Shape of You", artist="Ed Sheeran", genre="Pop", duration=234),
        Song(title="Bohemian Rhapsody", artist="Queen", genre="Rock", duration=354),
        Song(title="Uptown Funk", artist="Bruno Mars", genre="Funk", duration=270),
        Song(title="Someone Like You", artist="Adele", genre="Soul", duration=285),
    ]
    db.add_all(sample_songs)
    db.commit()
    return {"message": "Sample songs added", "count": len(sample_songs)}