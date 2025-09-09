from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

ALGORITHM_ENCODING = "HS256"
ACCESS_TOKEN_DURATION = 1 # minuto
SECRET = "SYGCJLKAXKHSLXaSLÑaXÑKDVHSL" # Clave secreta para firmar el token

router = APIRouter(tags=["JWT Auth User"]) # Etiqueta para la documentación
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool

class UserDB(User):
    password: str

# Simular una base de datos
users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe.dev",
        "disabled": False,
        "password": "$2a$12$mezshoUVqODJJiw2CqOuV.qTp.sgXrRe26gq8LWifBC.FrejegRqW"
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice.dev",
        "disabled": False,
        "password": "$2a$12$3Sc2CtNdTHDE1vNN6qmMJ.zRAvrc/jjLZAaeEj7raMSLcbYjRqi/G"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)): # Depende del oauth2
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM_ENCODING).get("sub") # sub porque es el campo que tiene el nombre en el acess_token
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticación inválidas.",
                            headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticación inválidas.",
                            headers={"WWW-Authenticate": "Bearer"})
    
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario inactivo.") 
    return user

@router.post("/login_jwt")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=404, detail="El usuario no es correcto.")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=404, detail="La contraseña no es correcta.")
    
    # Calcular expiración del token y generar el token
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION) 
    # Uso de datetime.now(timezone.utc) en vez de utcnow() (que está deprecated en 3.11 por no tener en cuenta zona horaria).
    access_token = {"sub": user.username, "exp": expire.timestamp()} 
    # sub es el nombre del usuario en el token, exp es la expiración del token (timestamp en segundos)

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM_ENCODING), "token_type": "bearer"}

@router.get("/users/me_jwt")
async def me(user: User = Depends(current_user)):
    return user