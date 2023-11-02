from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router.auth.router import router as auth_router
from router.home.router import router as home_router
from router.collections.router import router as collections_router
import uvicorn

app = FastAPI(title='Spotifly')

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(home_router)
app.include_router(collections_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)