from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.song import Song
from app.schemas.song import SongCreate, SongUpdate


def get_songs(db: Session, limit: int = 20, offset: int = 0) -> List[Song]:
    return db.query(Song).limit(limit).offset(offset).all()


def get_song_by_id(db: Session, song_id: int) -> Song | None:
    return db.query(Song).filter(Song.id == song_id).first()


def search_songs(db: Session, title: str, limit: int = 20, offset: int = 0) -> List[Song]:
    return db.query(Song).filter(Song.title.ilike(f"%{title}%")).limit(limit).offset(offset).all()


def create_song(db: Session, payload: SongCreate) -> Song:
    song = Song(
        title=payload.title,
        artist_id=payload.artist_id,
        album=payload.album,
        duration=payload.duration,
        thumbnail_url=str(payload.thumbnail_url) if payload.thumbnail_url else None,
    )
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


def update_song(db: Session, song: Song, payload: SongUpdate) -> Song:
    if payload.title is not None:
        song.title = payload.title
    if payload.artist_id is not None:
        song.artist_id = payload.artist_id
    if payload.album is not None:
        song.album = payload.album
    if payload.duration is not None:
        song.duration = payload.duration
    if payload.thumbnail_url is not None:
        song.thumbnail_url = str(payload.thumbnail_url)
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


def delete_song(db: Session, song: Song) -> None:
    db.delete(song)
    db.commit()


def build_stream_payload(song: Song) -> dict:
    stream_url = f"https://streaming.example.com/songs/{song.id}"  # placeholder streaming URL
    return {
        "id": song.id,
        "title": song.title,
        "stream_url": stream_url,
    }
