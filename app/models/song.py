from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id", ondelete="CASCADE"), nullable=False, index=True)
    album = Column(String(255), nullable=True)
    duration = Column(Integer, nullable=False)
    thumbnail_url = Column(String(512), nullable=True)

    artist = relationship("Artist", back_populates="songs")
