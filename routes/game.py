from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from random import sample
from database import get_db
from models import User, Transaction
from routes.auth import get_current_user  # Assurez-vous que ce chemin est correct

router = APIRouter()

COST_PER_LOT = 50  # Prix minimum par lot de 2 numéros
WIN_MULTIPLIER_TOP = 1000  # Multiplicateur si le lot est dans les 5 premiers numéros
WIN_MULTIPLIER_BOTTOM = 100  # Multiplicateur si le lot est dans les 5 seconds numéros

@router.post("/play")
def play_game(bets: list[dict], current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if len(bets) > 5:
        raise HTTPException(status_code=400, detail="Vous ne pouvez sélectionner que 5 lots maximum.")
    
    total_bet = sum(bet["amount"] for bet in bets)
    if current_user.balance < total_bet:
        raise HTTPException(status_code=400, detail="Solde insuffisant.")
    
    # Générer les numéros aléatoires du jeu
    top_numbers = sample(range(1, 100), 5)  # Génère 5 numéros pour le premier lot (haut)
    bottom_numbers = sample(range(1, 100), 5)  # Génère 5 numéros pour le deuxième lot (bas)
    
    winnings = 0
    
    # Vérification des gains pour chaque pari de l'utilisateur
    for bet in bets:
        numbers = sorted(bet["numbers"])  # Trier les numéros pour éviter les doublons
        amount = bet["amount"]
        
        # Vérifier si les deux numéros du lot sont dans le groupe haut
        if all(num in top_numbers for num in numbers):
            winnings += amount * WIN_MULTIPLIER_TOP
        
        # Vérifier si les deux numéros du lot sont dans le groupe bas
        elif all(num in bottom_numbers for num in numbers):
            winnings += amount * WIN_MULTIPLIER_BOTTOM
    
    # Mettre à jour le solde de l'utilisateur
    current_user.balance -= total_bet
    current_user.balance += winnings
    
    # Enregistrer la transaction
    db.add(Transaction(user_id=current_user.id, amount=-total_bet, transaction_type="bet"))
    if winnings > 0:
        db.add(Transaction(user_id=current_user.id, amount=winnings, transaction_type="win"))
    
    db.commit()
    
    return {
        "top_numbers": top_numbers,
        "bottom_numbers": bottom_numbers,
        "winnings": winnings,
        "new_balance": current_user.balance
    }
