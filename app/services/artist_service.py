from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.artist import Artist
from app.models.song import Song
from app.schemas.artist import ArtistCreate, ArtistUpdate


def get_artists(db: Session, limit: int = 20, offset: int = 0) -> List[Artist]:
    return db.query(Artist).limit(limit).offset(offset).all()


def get_artist_by_id(db: Session, artist_id: int) -> Artist | None:
    return db.query(Artist).filter(Artist.id == artist_id).first()


def search_artists(db: Session, name: str, limit: int = 20, offset: int = 0) -> List[Artist]:
    return db.query(Artist).filter(Artist.name.ilike(f"%{name}%")).limit(limit).offset(offset).all()


def create_artist(db: Session, payload: ArtistCreate) -> Artist:
    artist = Artist(name=payload.name)
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


def update_artist(db: Session, artist: Artist, payload: ArtistUpdate) -> Artist:
    if payload.name is not None:
        artist.name = payload.name
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


def delete_artist(db: Session, artist: Artist) -> None:
    db.delete(artist)
    db.commit()


def get_artist_songs(db: Session, artist_id: int, limit: int = 20, offset: int = 0) -> List[Song]:
    return db.query(Song).filter(Song.artist_id == artist_id).limit(limit).offset(offset).all()
