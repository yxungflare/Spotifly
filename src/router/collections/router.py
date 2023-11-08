from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from .models import Playlist
from router.auth.models import User
from router.auth.router import templates, db_dependency
from starlette import status

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
    return templates.TemplateResponse('base_playlist.html', {'request': request, 'username': username, 'playlist_id': playlist_id, 'playlist': current_playlist})