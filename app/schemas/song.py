from typing import Optional

from pydantic import BaseModel, HttpUrl


class SongBase(BaseModel):
    title: str
    artist_id: int
    album: Optional[str] = None
    duration: int
    thumbnail_url: Optional[HttpUrl] = None


class SongCreate(SongBase):
    pass


class SongUpdate(BaseModel):
    title: Optional[str] = None
    artist_id: Optional[int] = None
    album: Optional[str] = None
    duration: Optional[int] = None
    thumbnail_url: Optional[HttpUrl] = None


class SongRead(SongBase):
    id: int

    class Config:
        from_attributes = True


class SongStream(BaseModel):
    id: int
    title: str
    stream_url: HttpUrl

    class Config:
        from_attributes = True
