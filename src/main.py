from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from auth.router import router as auth_router
from home.router import router as home_router
import uvicorn

app = FastAPI(title='Spotifly')

app.include_router(auth_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(home_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)