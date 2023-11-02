from fastapi import APIRouter, Request
from sqlalchemy import select
from .models import Playlist
from router.auth.models import User
from router.auth.router import templates, db_dependency

router = APIRouter(
    prefix='/collections',
    tags=['Collections']
)


@router.get('/{username}')
async def get_collections_page(request: Request, username: str, db: db_dependency):
    playlists = await db.execute(select(Playlist).join(User).where(User.username == username))
    playlists_list = playlists.scalars().all()
    return templates.TemplateResponse('collections.html', {'request': request, 'username': username, 'playlists': playlists_list})