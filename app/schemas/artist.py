from pydantic import BaseModel


class ArtistBase(BaseModel):
    name: str


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(BaseModel):
    name: str | None = None


class ArtistRead(ArtistBase):
    id: int

    class Config:
        from_attributes = True
