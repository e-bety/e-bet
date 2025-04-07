from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from database import get_db  # ✅ OK
# ⚠️ Ne pas importer models ici pour éviter la boucle

# Charger les variables d'environnement
load_dotenv()

# 🔑 Secret Key et Configuration JWT
SECRET_KEY = os.getenv("SECRET_KEY", "monsecretjwt")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# 🔐 Configuration du hashing des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 Initialisation du schéma OAuth2 pour récupérer le token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 🔹 Fonction pour hasher un mot de passe
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 🔹 Fonction pour vérifier un mot de passe
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 🔹 Fonction pour générer un token JWT
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔹 Fonction pour récupérer l'utilisateur à partir du token JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from models import User  # ✅ Import ici pour éviter l'erreur circulaire

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Impossible de valider les identifiants",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Utilisateur non trouvé",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user  # ✅ Retourne l'objet User

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
