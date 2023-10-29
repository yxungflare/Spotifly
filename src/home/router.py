from fastapi import APIRouter, Request
from auth.router import templates

router = APIRouter(
    prefix='/home',
    tags=['Main page']
)

@router.get('')
async def get_main_page(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})