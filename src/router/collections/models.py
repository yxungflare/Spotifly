from sqlalchemy import BLOB, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

import datetime

from database import Base



class Playlist(Base):
    __tablename__ = 'playlist'

    id: Mapped[int] = mapped_column(
        Integer, unique=True, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(length=150), nullable=False
    )
    username_id: Mapped[str] = mapped_column(
        ForeignKey('user.id'), unique=True
    )
    songs_count: Mapped[int] = mapped_column(
        Integer, unique=False, default= 0
    ) 
    creation_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow()
    )
    cover:  Mapped[str] = mapped_column(
        String, default='/img/playlists/favorite.jpg'
    )


class Song(Base):
    __tablename__ = 'song'

    id: Mapped[int] = mapped_column(
        Integer, unique=True, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(length=150), unique=True, nullable=False
    )
    username_id: Mapped[str] = mapped_column(
        ForeignKey('user.id'), unique=False
    )
    playlist_id: Mapped[str] = mapped_column(
        ForeignKey('playlist.id'), unique=False
    )
    author_id: Mapped[str] = mapped_column(
        ForeignKey('author.id'), unique=False
    )
    albom_id: Mapped[str] = mapped_column(
        ForeignKey('albom.id'), unique=False
    )
    duration_song: Mapped[int] = mapped_column(
        Integer, unique=False
    ) 
    creation_date: Mapped[datetime.datetime] = mapped_column(
        nullable=True, default=datetime.datetime.utcnow()
    )
    

class Author(Base):
    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(
        Integer, unique=True, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(length=150), unique=True, nullable=False
    )
    

class Albom(Base):
    __tablename__ = 'albom'

    id: Mapped[int] = mapped_column(
        Integer, unique=True, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(length=150), unique=True, nullable=False
    )
    creation_date: Mapped[datetime.datetime] = mapped_column(
        nullable=True, default=datetime.datetime.utcnow()
    )
    author_id: Mapped[str] = mapped_column(
        ForeignKey('author.id'), unique=False
    )