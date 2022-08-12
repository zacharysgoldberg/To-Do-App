from fastapi import FastAPI, Depends
from models import Base
from database import engine
from routers import auth, todos, users
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette import status

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

# [extending the OAuth server and todos server to the main file server]
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
