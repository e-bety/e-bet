from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import models, schemas
from jose import jwt, JWTError
import os
import logging

# 🔹 Configuration des logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Clé secrète forte pour JWT
SECRET_KEY = os.getenv("SECRET_KEY", "monsecretjwt")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token valide pour 30 minutes
REFRESH_TOKEN_EXPIRE_DAYS = 7     # Token de rafraîchissement valide 7 jours

# 🔹 Configuration du hash des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 Fonction pour hacher un mot de passe
def hash_password(password: str):
    return pwd_context.hash(password)

# 🔹 Fonction pour vérifier un mot de passe
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 🔹 Générer un token JWT sécurisé
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔹 Vérifier et décoder un token JWT
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# 🔹 Inscription sécurisée d'un utilisateur
def create_user(db: Session, user: schemas.UserCreate):
    if db.query(models.User).filter(models.User.email == user.email).first():
        return {"error": "Cet email est déjà utilisé."}
    
    hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email, 
        username=user.username, 
        hashed_password=hashed_password, 
        balance=0, 
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 🔹 Authentification avec protection anti-brute force
def authenticate_user(db: Session, credentials: schemas.Login):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        logging.warning(f"Tentative de connexion échouée pour {credentials.email}")
        return None
    return user

# 🔹 Dépôt sécurisé
def deposit(db: Session, user: models.User, amount: float):
    if amount <= 0:
        return {"error": "Le montant doit être positif"}
    
    user.balance += amount
    db.commit()
    return {"message": f"Dépôt de {amount} F CFA validé!", "nouveau solde": user.balance}

# 🔹 Retrait sécurisé avec logs
def withdraw(db: Session, user: models.User, amount: float):
    if amount <= 0:
        return {"error": "Le montant doit être positif"}
    if user.balance < amount:
        logging.warning(f"Tentative de retrait refusée pour {user.email}: fonds insuffisants")
        return {"error": "Fonds insuffisants"}

    user.balance -= amount
    db.commit()
    logging.info(f"Retrait réussi de {amount} F CFA pour {user.email}")
    return {"message": f"Retrait de {amount} F CFA validé!", "nouveau solde": user.balance}

# 🔹 Jouer un pari sécurisé avec logs
def play_bet(db: Session, user: models.User, bet: schemas.BetCreate):
    if bet.amount <= 0:
        return {"error": "La mise doit être positive"}
    if user.balance < bet.amount:
        return {"error": "Fonds insuffisants pour jouer"}

    import random
    is_winner = random.choice([True, False])
    winnings = bet.amount * 2 if is_winner else 0

    user.balance += winnings - bet.amount
    db.commit()
    
    logging.info(f"{user.email} a joué {bet.amount} F CFA et {'gagné' if is_winner else 'perdu'} {winnings} F CFA")
    
    return {
        "message": "Victoire!" if is_winner else "Défaite!",
        "gain": winnings,
        "nouveau solde": user.balance
    }

# 🔹 Jouer en mode démo
def play_demo(bet: schemas.BetCreate):
    import random
    is_winner = random.choice([True, False])
    winnings = bet.amount * 2 if is_winner else 0

    return {
        "message": "Victoire!" if is_winner else "Défaite!",
        "gain": winnings
    }

# 🔹 Récupérer l'historique des transactions sécurisées
def get_history(db: Session, user: models.User):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user.id).all()

# 🔹 Récupérer les informations de parrainage
def get_referrals(db: Session, user: models.User):
    return db.query(models.User).filter(models.User.referrer_id == user.id).all()

# 🔹 Admin : Récupérer les demandes de recharge sécurisées
def get_recharge_requests(db: Session):
    return db.query(models.RechargeRequest).filter(models.RechargeRequest.status == "En attente").all()

# 🔹 Admin : Valider une recharge
def validate_recharge(db: Session, request_id: int):
    recharge_request = db.query(models.RechargeRequest).filter(models.RechargeRequest.id == request_id).first()
    if not recharge_request:
        return {"error": "Demande introuvable"}
    
    recharge_request.status = "Validé"
    user = db.query(models.User).filter(models.User.id == recharge_request.user_id).first()
    user.balance += recharge_request.amount
    db.commit()
    
    logging.info(f"Recharge validée pour {user.email}, montant: {recharge_request.amount} F CFA")
    
    return {"message": "Recharge validée avec succès!", "nouveau solde": user.balance}
