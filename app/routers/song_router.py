from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.database.session import get_session
from app.schemas.song import SongCreate, SongRead, SongStream, SongUpdate
from app.services.song_service import (
    build_stream_payload,
    create_song,
    delete_song,
    get_song_by_id,
    get_songs,
    search_songs,
    update_song,
)
from app.utils.dependencies import get_user_context, require_admin

router = APIRouter(prefix="/songs", dependencies=[Depends(get_user_context)])
admin_router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(get_user_context)])


@router.get("", response_model=dict,tags=['users',"admin"])
def list_songs(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_session),
) -> dict:
    songs = get_songs(db, limit=limit, offset=offset)
    return {"success": True, "data": jsonable_encoder(songs)}


@router.get("/search",tags=['users'], response_model=dict)
def search_song_by_title(
    title: str,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_session),
) -> dict:
    songs = search_songs(db, title, limit=limit, offset=offset)
    return {"success": True, "data": jsonable_encoder(songs)}


@router.get("/{song_id}",tags=['users'], response_model=dict)
def retrieve_song(
    song_id: int,
    db: Session = Depends(get_session),
) -> dict:
    song = get_song_by_id(db, song_id)
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    return {"success": True, "data": jsonable_encoder(song)}


@router.get("/{song_id}/stream",tags=['users',"admin"], response_model=dict)
def stream_song(
    song_id: int,
    db: Session = Depends(get_session),
) -> dict:
    song = get_song_by_id(db, song_id)
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    payload = build_stream_payload(song)
    return {"success": True, "data": payload}


@router.post("",   tags=['admin'], response_model=dict, dependencies=[Depends(require_admin)])
def create_song_endpoint(
    payload: SongCreate,
    db: Session = Depends(get_session),
) -> dict:
    song = create_song(db, payload)
    return {"success": True, "data": jsonable_encoder(song), "message": "Song created"}


@router.put("/{song_id}",tags=['admin'], response_model=dict, dependencies=[Depends(require_admin)])
def update_song_endpoint(
    song_id: int,
    payload: SongUpdate,
    db: Session = Depends(get_session),
) -> dict:
    song = get_song_by_id(db, song_id)
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    updated = update_song(db, song, payload)
    return {"success": True, "data": jsonable_encoder(updated), "message": "Song updated"}


@router.delete("/{song_id}", tags=['admin'], response_model=dict, dependencies=[Depends(require_admin)])
def delete_song_endpoint(
    song_id: int,
    db: Session = Depends(get_session),
) -> dict:
    song = get_song_by_id(db, song_id)
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    delete_song(db, song)
    return {"success": True, "data": None, "message": "Song deleted"}


@admin_router.get("/songs",tags=['admin'], response_model=dict, dependencies=[Depends(require_admin)])
def admin_list_songs(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_session),
) -> dict:
    songs = get_songs(db, limit=limit, offset=offset)
    return {"success": True, "data": jsonable_encoder(songs)}
