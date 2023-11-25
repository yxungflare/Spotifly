from typing import Annotated
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from .models import Playlist, Song
from router.auth.models import User
from router.auth.router import templates, db_dependency
from starlette import status

from mutagen.mp3 import MP3

import os
import shutil

router = APIRouter(
    prefix='/collections',
    tags=['Collections']
)


@router.get('/{username}')
async def get_collections_page(request: Request, username: str, db: db_dependency):
    playlists = await db.execute(select(Playlist).join(User).where(User.username == username))
    playlists_list = playlists.scalars().all()


    favorite_playlists_couter = 0
    for playlist in playlists_list:
        if playlist.is_liked:
            favorite_playlists_couter += 1
    print(favorite_playlists_couter)
    return templates.TemplateResponse('collections.html', {'request': request, 'username': username, 'playlists': playlists_list, 'favorite_playlists_couter': favorite_playlists_couter})


@router.post('/{username}/playlist/new', status_code=status.HTTP_201_CREATED)
async def create_new_playlist(request: Request, username: str, db: db_dependency):
    user = await db.execute(select(User).where(User.username == username))
    current_user = user.scalar()

    new_playlist = Playlist(
        name = 'Новый плейлист',
        username_id = current_user.id,
    )
    
    db.add(new_playlist)
    await db.commit()
    return RedirectResponse(url=f"/collections/{username}/playlist/{new_playlist.id}", status_code=303)

@router.get('/{username}/playlist/{playlist_id}')
async def get_collections_page(request: Request, username: str, playlist_id: int, db: db_dependency):
    playlist = await db.execute(select(Playlist).where(Playlist.id == playlist_id).join(User).where(User.username == username))
    current_playlist = playlist.scalar()

    songs = await db.execute(select(Song).join(User).where(User.username == username).join(Playlist).where(Playlist.id == playlist_id))
    songs_list = songs.scalars().all()

    return templates.TemplateResponse('base_playlist.html', {'request': request, 'username': username, 'playlist': current_playlist, 'songs': songs_list})


@router.post('/{username}/playlist/{playlist_id}/add_description', status_code=status.HTTP_201_CREATED)
async def add_playlist_description(request: Request, username: str, playlist_id: int, db: db_dependency, description: Annotated[str, Form()]):
    playlist = await db.execute(select(Playlist).where(Playlist.id == playlist_id).join(User).where(User.username == username))
    current_playlist = playlist.scalar()
    current_playlist.description = description

    await db.commit()

    return RedirectResponse(url=f"/collections/{username}/playlist/{playlist_id}", status_code=303)


@router.post('/{username}/playlist/{playlist_id}/edit_description', status_code=status.HTTP_205_RESET_CONTENT)
async def edit_playlist_description(request: Request, username: str, playlist_id: int, db: db_dependency, description: Annotated[str, Form()]):
    playlist = await db.execute(select(Playlist).where(Playlist.id == playlist_id).join(User).where(User.username == username))
    current_playlist = playlist.scalar()
    current_playlist.description = description

    await db.commit()

    return RedirectResponse(url=f"/collections/{username}/playlist/{playlist_id}", status_code=303)


@router.post('/{username}/playlist/{playlist_id}/edit_playlist_name', status_code=status.HTTP_205_RESET_CONTENT)
async def edit_playlist_name(request: Request, username: str, playlist_id: int, db: db_dependency, name: Annotated[str, Form()]):
    playlist = await db.execute(select(Playlist).where(Playlist.id == playlist_id).join(User).where(User.username == username))
    current_playlist = playlist.scalar()
    current_playlist.name = name

    await db.commit()

    return RedirectResponse(url=f"/collections/{username}/playlist/{playlist_id}", status_code=303)


@router.post('/{username}/playlist/{playlist_id}/edit_playlist_cover', status_code=status.HTTP_205_RESET_CONTENT)
async def edit_playlist_cover(request: Request, username: str, playlist_id: int, db: db_dependency,  cover: UploadFile = File()):
    upload_folder = f"./static/img/playlists/{username}/{str(playlist_id)}"

    cover.filename = 'playlist_cover'

    static = f'/img/playlists/{username}/{str(playlist_id)}'
    # Создаем директорию, если она не существует
    os.makedirs(upload_folder, exist_ok=True)

    # Полный путь к файлу
    file_path = os.path.join(upload_folder, cover.filename)

    # Записываем файл
    with open(file_path, "wb") as file:
        shutil.copyfileobj(cover.file, file)

    playlist = await db.execute(select(Playlist).where(Playlist.id == playlist_id).join(User).where(User.username == username))
    current_playlist = playlist.scalar()
    current_playlist.cover = f'{static}/{cover.filename}' 

    await db.commit()

    return RedirectResponse(url=f"/collections/{username}/playlist/{playlist_id}", status_code=303)


@router.delete('/{username}/playlist/{playlist_id}/delete', status_code=status.HTTP_205_RESET_CONTENT)
async def delete_current_playlist(request: Request, username: str, playlist_id: int, db: db_dependency):
    
    playlist = await db.execute(select(Playlist).where(Playlist.id == playlist_id).join(User).where(User.username == username))
    current_playlist = playlist.scalar()
    await db.delete(current_playlist)

    await db.commit()

    return RedirectResponse(url=f"/collections/{username}", status_code=303)


@router.post('/{username}/playlist/{playlist_id}/make_favorite', status_code=status.HTTP_205_RESET_CONTENT)
async def make_favorite(request: Request, username: str, playlist_id: int, db: db_dependency):
    playlist = await db.execute(select(Playlist).where(Playlist.id == playlist_id).join(User).where(User.username == username))
    current_playlist = playlist.scalar()

    current_playlist.is_liked = True
    
    await db.commit()


@router.post('/{username}/playlist/{playlist_id}/make_not_favorite', status_code=status.HTTP_205_RESET_CONTENT)
async def make_not_favorite(request: Request, username: str, playlist_id: int, db: db_dependency):
    playlist = await db.execute(select(Playlist).where(Playlist.id == playlist_id).join(User).where(User.username == username))
    current_playlist = playlist.scalar()

    current_playlist.is_liked = False
    
    await db.commit()


@router.post('/{username}/playlist/{playlist_id}/add_song', status_code=status.HTTP_205_RESET_CONTENT)
async def add_song_to_playlist(request: Request, username: str, playlist_id: int, db: db_dependency,  song: UploadFile = File()):
    # Сначала сохраняем файл
    upload_folder = f"./static/songs/playlists/{username}/{str(playlist_id)}"

    # Создаем директорию, если она не существует
    os.makedirs(upload_folder, exist_ok=True)

    # Добавляем к созданной директории имя файла для создания полного пути
    file_path = os.path.join(upload_folder, song.filename)

    # Записываем файл
    with open(file_path, "wb") as file:
        shutil.copyfileobj(song.file, file)


    # Затем добавляем его в базу данных

    # Определяем текущего пользователя
    user = await db.execute(select(User).where(User.username == username))
    current_user = user.scalar()

    # Определяем текущий плейлист
    playlist = await db.execute(select(Playlist).where(Playlist.id == playlist_id).join(User).where(User.username == username))
    current_playlist = playlist.scalar()

    # Добавляем песню в ДБ
    added_song = Song(
        name = song.filename,
        username_id = current_user.id,
        playlist_id = current_playlist.id,
        duration_song = format_duration_song((MP3(song.file).info.length)),
    )
    
    db.add(added_song)
    await db.commit()

    return RedirectResponse(url=f"/collections/{username}/playlist/{playlist_id}", status_code=303)


def format_duration_song(duration):
    minutes, seconds = divmod(duration, 60)
    return f'{str(int(minutes))}:{str(int(seconds))}'