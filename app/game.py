from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from random import sample
from app import models, schemas, database
from app.auth import get_current_user
from app.schemas import BetRequest  


router = APIRouter(prefix="/game", tags=["game"])

# Prix minimum par lot
LOT_PRICE = 50  

@router.post("/play")
def play_game(
    bet_data: BetRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Permet à un utilisateur de jouer en misant sur des lots de 2 numéros.
    Génère deux groupes de 5 nombres aléatoires et calcule les gains selon les règles officielles.
    """
    # Vérifier si l'utilisateur a assez d'argent pour jouer
    total_bet = sum(lot.amount for lot in bet_data.lots)
    if total_bet > current_user.balance:
        raise HTTPException(status_code=400, detail="Solde insuffisant.")

    # Génération des numéros aléatoires
    all_numbers = sample(range(1, 100), 10)
    first_group = all_numbers[:5]  # Premier groupe (haut)
    second_group = all_numbers[5:]  # Deuxième groupe (bas)

    # Calcul des gains
    total_winnings = 0
    for lot in bet_data.lots:
        num1, num2 = lot.numbers
        bet_amount = lot.amount
        gain_multiplier = 0

        # Vérifier si le lot correspond aux règles
        lot_set = {num1, num2}  # Ensemble pour ignorer l'ordre des numéros

        # 🏆 **Multiplication x1000** → Si les deux numéros sont exactement les deux premiers du premier groupe (peu importe l'ordre)
        if lot_set == {first_group[0], first_group[1]}:
            gain_multiplier = 1000
        # 🔥 **Multiplication x100** → Si les 2 numéros sont présents dans les 5 numéros du premier groupe (peu importe l'ordre)
        elif num1 in first_group and num2 in first_group:
            gain_multiplier = 100
        # 🎯 **Multiplication x50** → Si les 2 numéros sont présents dans les 5 numéros du deuxième groupe (peu importe l'ordre)
        elif num1 in second_group and num2 in second_group:
            gain_multiplier = 50
        # 🔁 **Multiplication x25** → Si un numéro est dans le premier groupe et l'autre dans le deuxième, et que les indices sont égaux
        elif (num1 in first_group and num2 in second_group) or (num2 in first_group and num1 in second_group):
            index1 = first_group.index(num1) if num1 in first_group else second_group.index(num1)
            index2 = second_group.index(num2) if num2 in second_group else first_group.index(num2)
            if index1 == index2:
                gain_multiplier = 25
        # 💰 **Multiplication x200** → Si un numéro est le premier du premier groupe et l'autre est le dernier du deuxième groupe
        elif (num1 == first_group[0] and num2 == second_group[-1]) or (num2 == first_group[0] and num1 == second_group[-1]):
            gain_multiplier = 200
        # 🔥 **Multiplication x150** → Si un numéro est le dernier du premier groupe et l'autre est le premier du deuxième groupe
        elif (num1 == first_group[-1] and num2 == second_group[0]) or (num2 == first_group[-1] and num1 == second_group[0]):
            gain_multiplier = 150

        # Calcul du gain total
        total_winnings += bet_amount * gain_multiplier

    # Mise à jour du solde de l'utilisateur
    current_user.balance -= total_bet
    current_user.balance += total_winnings
    db.commit()

    # Sauvegarde de la transaction
    new_transaction = models.Transaction(
        user_id=current_user.id,
        amount=total_winnings - total_bet,  # Gain net
        transaction_type="bet"
    )
    db.add(new_transaction)
    db.commit()

    return {
        "message": "Jeu terminé.",
        "generated_numbers": {
            "first_group": first_group,
            "second_group": second_group
        },
        "total_winnings": total_winnings,
        "new_balance": current_user.balance
    }
