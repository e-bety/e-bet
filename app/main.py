from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware  # Ajout du middleware CORS
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.schemas import TransactionRequest, RegisterRequest, BetRequest
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models import User, ReferralBonus, Bet, RechargeRequest, Transaction
from datetime import timedelta
from app.auth import router as auth_router
from app.jeu import router as jeu_router
from app.routes.transactions import router as transaction_router
from fastapi.responses import RedirectResponse
from typing import List
from app.game import play_game
from app.auth import get_current_user, create_access_token
from pydantic import BaseModel
from app.cinetpay import notify_payment  # Assurer que cette fonction est bien définie dans cinetpay.py
from app.cinetpay import router as cinetpay_router  # Route de cinetpay
from app.auth import router as auth_router
from app.payment import router as payment_router  # Assurer que payment_router est bien défini
import requests
import logging
import decimal
import random
import os
from passlib.context import CryptContext


app = FastAPI()

# Assure-toi que les routes sont bien inclues dans l'application
app.include_router(auth_router, prefix="/auth")
app.include_router(payment_router, prefix="/payment")  # Assurer que payment_router est correctement importé
app.include_router(cinetpay_router, prefix="/cinetpay")  # Route pour gérer les notifications CinetPay
app.include_router(jeu_router)
app.include_router(transaction_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ✅ Autoriser le frontend à accéder à l'API (évite les erreurs CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Autorise toutes les origines (à restreindre en prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Contexte de hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ✅ Route de test pour le jeu
@app.get("/jouer")
def jouer(user_id: int, bet_amount: int, db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.id == user_id).first()
    if not current_user:
        return {"error": "Utilisateur non trouvé"}

    if current_user.balance < bet_amount:
        return {"error": "Solde insuffisant"}

    first_group = random.sample(range(1, 100), 5)
    second_group = random.sample(range(1, 100), 5)

    user_lots = [(random.randint(1, 99), random.randint(1, 99)) for _ in range(5)]

    total_winnings = 0

    for num1, num2 in user_lots:
        gain_multiplier = 0
        if {num1, num2} == {first_group[0], first_group[1]}:
            gain_multiplier = 1000
        elif num1 in first_group and num2 in first_group:
            gain_multiplier = 100
        elif num1 in second_group and num2 in second_group:
            gain_multiplier = 50
        elif (num1 in first_group and num2 in second_group) or (num2 in first_group and num1 in second_group):
            index1 = first_group.index(num1) if num1 in first_group else second_group.index(num1)
            index2 = second_group.index(num2) if num2 in second_group else first_group.index(num2)
            if index1 == index2:
                gain_multiplier = 25
        elif (num1 == first_group[0] and num2 == second_group[-1]) or (num2 == first_group[0] and num1 == second_group[-1]):
            gain_multiplier = 200
        elif (num1 == first_group[-1] and num2 == second_group[0]) or (num2 == first_group[-1] and num1 == second_group[0]):
            gain_multiplier = 150

        total_winnings += bet_amount * gain_multiplier

    current_user.balance -= bet_amount * 5
    current_user.balance += total_winnings
    db.commit()

    return {
        "resultat": f"Tirage effectué! Numéros gagnants: {first_group} / {second_group}",
        "gain": total_winnings,
        "nouveau_solde": current_user.balance
    }

@app.post("/register")
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")

    referrer = None
    if user_data.referrer_id:
        referrer = db.query(User).filter(User.id == user_data.referrer_id).first()
        if not referrer:
            raise HTTPException(status_code=400, detail="Parrain invalide")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_password,
        balance=decimal.Decimal("0.00"),
        referrer_id=user_data.referrer_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Compte créé avec succès !"}

def create_payment(amount: float, phone_number: str):
    url = "https://api.cinetpay.com/v1/payment"
    data = {
        "amount": amount,
        "phone_number": phone_number,
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        return response.json().get('payment_url')
    else:
        raise Exception("Erreur lors de la création du paiement")

# 🎮 Mode démo pour tester le jeu
@app.post("/play-demo")
def play_demo(bets: List[BetRequest], db: Session = Depends(get_db)):
    demo_user = User(id=0, username="Demo", balance=999999)  # Faux utilisateur
    result = play_game(demo_user, bets, is_demo=True, db=db)
    return result

@app.get("/ping")
def ping():
    return {"message": "pong"}

# 🏁 Historique des paris
@app.get("/history")
def get_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bets = db.query(Bet).filter(Bet.user_id == current_user.id).order_by(Bet.timestamp.desc()).all()

    return {
        "user": current_user.username,
        "history": [
            {
                "bet_id": bet.id,
                "numbers": bet.numbers,
                "bet_amount": float(bet.bet_amount),
                "result": bet.result,
                "winnings": float(bet.winnings),
                "is_demo": bool(bet.is_demo),
                "first_group": bet.first_group,
                "second_group": bet.second_group,
                "timestamp": bet.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for bet in bets
        ],
    }

# ✅ Route pour voir les filleuls et bonus
@app.get("/referrals")
def get_referrals(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    direct_referrals = db.query(User).filter(User.referrer_id == current_user.id).all()
    total_bonus = db.query(ReferralBonus).filter(ReferralBonus.referrer_id == current_user.id).count()

    return {
        "total_filleuls": len(direct_referrals),
        "total_gains": total_bonus,
        "filleuls": [{"id": user.id, "username": user.username} for user in direct_referrals]
    }
