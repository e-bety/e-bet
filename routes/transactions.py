from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Transaction
from database import SessionLocal
from auth import oauth2_scheme
from jose import jwt, JWTError

SECRET_KEY = "monsecretjwt"
ALGORITHM = "HS256"

router = APIRouter()

# Fonction pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fonction pour récupérer l'utilisateur connecté
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
    
    return user

# 🔹 Route pour effectuer un dépôt
@router.post("/deposit/")
def deposit(amount: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Le montant doit être supérieur à 0")

    # Mise à jour du solde utilisateur
    current_user.balance += amount
    db.add(Transaction(user_id=current_user.id, amount=amount, transaction_type="deposit"))
    db.commit()

    return {"message": f"Dépôt de {amount} effectué avec succès", "nouveau_solde": current_user.balance}

# 🔹 Route pour effectuer un retrait
@router.post("/withdraw/")
def withdraw(amount: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Le montant doit être supérieur à 0")

    if current_user.balance < amount:
        raise HTTPException(status_code=400, detail="Fonds insuffisants")

    # Mise à jour du solde utilisateur
    current_user.balance -= amount
    db.add(Transaction(user_id=current_user.id, amount=amount, transaction_type="withdrawal"))
    db.commit()

    return {"message": f"Retrait de {amount} effectué avec succès", "nouveau_solde": current_user.balance}

# 🔹 Route pour consulter l'historique des transactions
@router.get("/transactions/")
def get_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    return transactions
