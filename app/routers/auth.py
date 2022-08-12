from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form
from typing import Optional
from models import Users, Base
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

SECRET_KEY = '3K75JD2JKDS99U342YINQ0'

ALGORITHM = "HS256"

templates = Jinja2Templates(directory="templates")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Base.metadata.create_all(bind=engine)

oatuh2_bearer = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.pasword: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get('email')
        self.password = form.get('password')


def hash_password(password):
    return bcrypt_context.hash(password)


def verify_password(password, hashed_password):
    return bcrypt_context.verify(password, hashed_password)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user

# [create an encoded JWT]


def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# [decode JWT]


async def get_current_user(request: Request):
    try:
        token = request.cookies.get('access_token')
        if token is None:
            return None

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            logout(request)

        return {'username': username, 'id': user_id}

    except JWTError:
        raise HTTPException(status_code=404, detail="Not found")


@router.post('/token')
async def login_for_access_token(response: Response,
                                 form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return False
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)

    response.set_cookie(key="access_token", value=token, httponly=True)

    return True


@router.get('/', response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post('/', response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(
            url="/todos", status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(response=response, form_data=form, db=db)

        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})

        return response
    except HTTPException:
        msg = "Unknown Error"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.get('/logout')
async def logout(request: Request, db: Session = Depends(get_db)):
    msg = "Logout Successful"
    response = templates.TemplateResponse(
        "login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")

    return response


@router.get('/register', response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post('/register', response_class=HTMLResponse)
async def register_user(request: Request, email: str = Form(...), username: str = Form(...),
                        firstname: str = Form(...), lastname: str = Form(...),
                        password: str = Form(...), password2: str = Form(...),
                        db: Session = Depends(get_db)):
    validate_username = db.query(Users).filter(
        Users.username == username).first()
    validate_email = db.query(Users).filter(Users.email == email).first()

    if password != password2 or validate_username is not None or validate_email is not None:
        msg = "Invalid registration request"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})

    user_model = Users()
    user_model.email = email
    user_model.username = username
    user_model.first_name = firstname
    user_model.last_name = lastname

    hashed_password = hash_password(password)
    user_model.password = hashed_password
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    msg = "User successfully created"
    return templates.TemplateResponse('login.html', {"request": request, "msg": msg})
