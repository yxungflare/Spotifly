import asyncio
from typing import Annotated
import asyncpg
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse
from sqlalchemy import select
import sqlalchemy
from .models import Playlist, Song, Author
from router.auth.models import User
from router.auth.router import templates, db_dependency
from starlette import status

from mutagen.mp3 import MP3
import eyed3

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
    
    playlists = await db.execute(select(Playlist).join(User).where(User.username == username))
    playlists_list = playlists.scalars().all()

    playlist_dict = dict()
    for p in playlists_list:
        playlist_dict[p.id] = p.name

    playlist_id_array = []

    for playlist in playlists_list:
        playlist_id_array.append(playlist.id)

    songs_list = (await db.execute(
        select(Song, Author.name.label('author_name'))
        .join(User)
        .where(User.username == username)
        .join(Author)
        .where(Song.author_id == Author.id)
    )).all()

    songs_couter = 1
    if len(songs_list) == 0:
        songs_couter = 0
    version = 1
    return templates.TemplateResponse('base_playlist.html', {'request': request, 'username': username, 'playlist': current_playlist, 'playlists': playlist_dict , 'playlist_id_array': playlist_id_array, 'songs': songs_list, 'songs_couter': songs_couter, 'version_songs_couter': version})


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
    
    # Выбираем плейлист
    playlist = await db.execute(select(Playlist).where(Playlist.id == playlist_id).join(User).where(User.username == username))
    current_playlist = playlist.scalar()

    # Удаляем все песни из плейлиста
    songs = await db.execute(select(Song).where(Song.playlist_id == playlist_id).join(User).where(User.username == username))
    songs_list = songs.scalars().all()

    for song in songs_list:
        song.playlist_id = None

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


def get_audio_metadata(file_path, a):
    audiofile = eyed3.load(file_path)

    if audiofile is not None:
        if a == 1:
            return audiofile.tag.title
        if a == 2:
            print(audiofile.tag.artist)
            return audiofile.tag.artist
        # print("Альбом:", audiofile.tag.album)
        # print("Год:", audiofile.tag.getBestDate())
        # Другие метаданные могут быть получены аналогичным образом

    else:
        print("Невозможно загрузить метаданные аудиофайла.")
    

async def get_author_id(db, file_path):
    author = await db.execute(select(Author).where(Author.name == get_audio_metadata(file_path, 2)))
    current_author = author.fetchone()
    if current_author is not None:
        return current_author[0].id
    author = Author(
        name = get_audio_metadata(file_path, 2)
    )
    db.add(author)
    await db.commit()

    author = await db.execute(select(Author).where(Author.name == get_audio_metadata(file_path, 2)))
    current_author = author.fetchone()

    return current_author[0].id

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
    print(song.filename)
    added_song = Song(
        name = get_audio_metadata(file_path, 1),
        filename = song.filename,
        username_id = current_user.id,
        playlist_id = current_playlist.id,
        author_id = await get_author_id(db, file_path),
        duration_song = format_duration_song((MP3(song.file).info.length)),
    )
    
    db.add(added_song)

    await db.commit()

    return RedirectResponse(url=f"/collections/{username}/playlist/{playlist_id}", status_code=303)


def format_duration_song(duration):
    minutes, seconds = divmod(duration, 60)
    return f'{str(int(minutes))}:{str(int(seconds))}'


# Поиск песни в плейлисте
@router.post('/{username}/playlist/{playlist_id}/find_song')
async def find_song_in_playlist(request: Request, username: str, playlist_id: int, db: db_dependency, song_name: Annotated[str, Form()]):
    
    # Определяем текущий плейлист
    playlist = await db.execute(select(Playlist).where(Playlist.id == playlist_id).join(User).where(User.username == username))
    current_playlist = playlist.scalar()
    
    # Находим песню в БД
    songs = (await db.execute(select(Song, Author.name.label('author_name')).where(Song.playlist_id == playlist_id).join(User).where(User.username == username).where(Song.name == song_name).join(Author).where(Song.author_id == Author.id))).all()

    songs_couter, version = 1, 2

    playlists = (await db.execute(select(Playlist).join(User).where(User.username == username)))
    playlists_list = playlists.scalars().all()

    playlist_dict = dict()
    for p in playlists_list:
        playlist_dict[p.id] = p.name

    return templates.TemplateResponse('base_playlist.html', {'request': request, 'username': username, 'playlists': playlist_dict, 'playlist': current_playlist, 'songs': songs, 'songs_couter': songs_couter, 'version_songs_couter': version})


# Удаляем песню с плейлиста
@router.delete('/{username}/playlist/{playlist_id}/delete_song/{song_id}', status_code=status.HTTP_205_RESET_CONTENT)
async def delete_song_from_playlist(request: Request, username: str, playlist_id: int, song_id: int, db: db_dependency):
    # Определяем текущий плейлист
    playlist = await db.execute(select(Playlist).where(Playlist.id == playlist_id).join(User).where(User.username == username))
    current_playlist = playlist.scalar()
    
    # Находим песню в БД
    song = await db.execute(select(Song).where(Song.id == song_id).join(User).where(User.username == username).join(Playlist).where(Playlist.id == playlist_id))
    current_song = song.scalar()
    
    await db.delete(current_song)
    await db.commit()

    return RedirectResponse(url=f"/collections/{username}/playlist/{playlist_id}", status_code=200)


@router.post('/{username}/playlist/{playlist_id}/add_song/{song_id}', status_code=status.HTTP_205_RESET_CONTENT)
async def add_song_to_another_playlist(request: Request, username: str, playlist_id: int, song_id: int, db: db_dependency):
    song = await db.execute(select(Song).where(Song.id == song_id).join(User).where(User.username == username).join(Playlist).where(Playlist.id == playlist_id))
    current_song = song.scalar()
    
    # Определяем текущего пользователя
    user = await db.execute(select(User).where(User.username == username))
    current_user = user.scalar()

    # Добавляем песню в ДБ
    added_song_to_another_playlist = Song(
        name = current_song.name,
        username_id = current_user.id,
        playlist_id = playlist_id,
        duration_song = current_song.duration_song,
    )

    db.add(added_song_to_another_playlist)
    await db.commit()

    return RedirectResponse(url=f"/collections/{username}/playlist/{playlist_id}", status_code=303)


@router.post('/{username}/make_favorite_song/{song_id}', status_code=status.HTTP_205_RESET_CONTENT)
async def add_song_to_favorites(request: Request, username: str, song_id: int, db: db_dependency):
    song = await db.execute(select(Song).where(Song.id == song_id).join(User).where(User.username == username))
    current_song = song.scalar()

    current_song.is_liked = True

    await db.commit()


@router.post('/{username}/make_not_favorite_song/{song_id}', status_code=status.HTTP_205_RESET_CONTENT)
async def add_song_to_not_favorites(request: Request, username: str, song_id: int, db: db_dependency):
    song = await db.execute(select(Song).where(Song.id == song_id).join(User).where(User.username == username))
    current_song = song.scalar()

    current_song.is_liked = False

    await db.commit()
