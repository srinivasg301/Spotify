from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.database.session import get_session
from app.schemas.artist import ArtistCreate, ArtistRead, ArtistUpdate
from app.schemas.song import SongRead
from app.services.artist_service import (
    create_artist,
    delete_artist,
    get_artist_by_id,
    get_artist_songs,
    get_artists,
    search_artists,
    update_artist,
)
from app.utils.dependencies import get_user_context, require_admin

router = APIRouter(prefix="/artists", dependencies=[Depends(get_user_context)])


@router.get("", tags=['users'], response_model=dict, status_code=status.HTTP_200_OK)
def list_artists(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_session),
) -> dict:
    artists = get_artists(db, limit=limit, offset=offset)
    return {"success": True, "data": jsonable_encoder(artists)}


@router.get("/search",tags=['users'], response_model=dict)
def search_artist_by_name(
    name: str,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_session),
) -> dict:
    results = search_artists(db, name, limit=limit, offset=offset)
    return {"success": True, "data": jsonable_encoder(results)}


@router.get("/{artist_id}", tags=['users'], response_model=dict)
def retrieve_artist(
    artist_id: int,
    db: Session = Depends(get_session),
) -> dict:
    artist = get_artist_by_id(db, artist_id)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return {"success": True, "data": jsonable_encoder(artist)}


@router.get("/{artist_id}/songs", tags=['users'], response_model=dict)
def list_artist_songs(
    artist_id: int,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_session),
) -> dict:
    artist = get_artist_by_id(db, artist_id)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    songs = get_artist_songs(db, artist_id, limit=limit, offset=offset)
    return {"success": True, "data": jsonable_encoder(songs)}


@router.post("", response_model=dict, tags=['admin'], dependencies=[Depends(require_admin)] )
def create_artist_endpoint(
    payload: ArtistCreate,
    db: Session = Depends(get_session),
) -> dict:
    artist = create_artist(db, payload)
    return {"success": True, "data": jsonable_encoder(artist), "message": "Artist created"}


@router.put("/{artist_id}",tags=['admin'], response_model=dict, dependencies=[Depends(require_admin)])
def update_artist_endpoint(
    artist_id: int,
    payload: ArtistUpdate,
    db: Session = Depends(get_session),
) -> dict:
    artist = get_artist_by_id(db, artist_id)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    updated = update_artist(db, artist, payload)
    return {"success": True, "data": jsonable_encoder(updated), "message": "Artist updated"}


@router.delete("/{artist_id}", response_model=dict, tags=['admin'], dependencies=[Depends(require_admin)])
def delete_artist_endpoint(
    artist_id: int,
    db: Session = Depends(get_session),
) -> dict:
    artist = get_artist_by_id(db, artist_id)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    delete_artist(db, artist)
    return {"success": True, "data": None, "message": "Artist deleted"}
