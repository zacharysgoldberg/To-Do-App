from fastapi import FastAPI
import uvicorn
# from models import Base
# from database import engine
from routers import auth, todos, users, forgot_password, register
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette import status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Base.metadata.create_all(bind=engine)

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

# [extending the OAuth server and todos server to the main file server]
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(forgot_password.router)
app.include_router(register.router)
