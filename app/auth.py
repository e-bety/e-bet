import os
import decimal
import logging
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.database import SessionLocal   
from app.models import User
from typing import Union

# 🔹 Charger les variables d'environnement
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "monsecretjwt")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# 🔹 Initialisation
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ✅ Fonction pour récupérer une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Création du token JWT
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Hachage du mot de passe
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ✅ Vérification du mot de passe
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Schéma Pydantic pour l'inscription
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    referrer_id: Union[int, None] = None

# ✅ Route d'inscription
@router.post("/register")
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        # Vérifier si le nom d'utilisateur est déjà pris
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            logging.error(f"Nom d'utilisateur déjà pris: {user_data.username}")
            raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")

        # Vérifier si l'email est déjà utilisé
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            logging.error(f"Email déjà utilisé: {user_data.email}")
            raise HTTPException(status_code=400, detail="Email déjà utilisé")

        # Vérification du parrain
        referrer = None
        if user_data.referrer_id:
            referrer = db.query(User).filter(User.id == user_data.referrer_id).first()
            if not referrer:
                logging.error(f"Parrain invalide: {user_data.referrer_id}")
                raise HTTPException(status_code=400, detail="Parrain invalide")

        hashed_password = get_password_hash(user_data.password)

        # Créer un nouvel utilisateur
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            balance=decimal.Decimal("0.00"),
            referrer_id=user_data.referrer_id
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return RedirectResponse(url="/login", status_code=303)

    except Exception as e:
        logging.error(f"Erreur lors de l'inscription: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'inscription")

# ✅ Route de connexion
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Récupération de l'utilisateur actuel via le token JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    return user

# ✅ Route pour récupérer l'utilisateur connecté
@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "balance": current_user.balance
    }
