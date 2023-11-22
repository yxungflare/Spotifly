from typing import Annotated
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from .models import Playlist
from router.auth.models import User
from router.auth.router import templates, db_dependency
from starlette import status

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
    return templates.TemplateResponse('collections.html', {'request': request, 'username': username, 'playlists': playlists_list})


@router.post('/{username}/playlist/new', status_code=status.HTTP_201_CREATED)
async def create_new_playlist(request: Request, username: str, db: db_dependency):
    result = await db.execute(select(User).where(User.username == username))
    current_user = result.scalar()

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
    return templates.TemplateResponse('base_playlist.html', {'request': request, 'username': username, 'playlist': current_playlist})


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
    