from fastapi import APIRouter, Request
from router.auth.router import templates

router = APIRouter(
    prefix='/home',
    tags=['Main page']
)


@router.get('')
async def get_main_page(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@router.get('/{username}')
async def get_auth_home_page(request: Request, username: str):
    return templates.TemplateResponse('home_auth.html', {'request': request, 'username': username})