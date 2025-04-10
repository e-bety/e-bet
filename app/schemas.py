from pydantic import BaseModel, Field
from typing import Optional

# ✅ Schéma pour l'inscription
class RegisterRequest(BaseModel):
    username: str
    email: str  # Ajout du champ email
    password: str
    referrer_id: int = None  # Le parrain est optionnel

    class Config:
        orm_mode = True
        
# ✅ Schéma pour la connexion
class LoginRequest(BaseModel):
    username: str
    password: str

# ✅ Schéma pour la réponse contenant un token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# ✅ Schéma pour récupérer le solde utilisateur
class BalanceResponse(BaseModel):
    username: str
    balance: float

# ✅ Schéma pour les transactions (dépôt/retrait)
class TransactionRequest(BaseModel):
    amount: float

# ✅ Schéma pour la réponse après une transaction
class TransactionResponse(BaseModel):
    message: str
    new_balance: float

# ✅ Schéma pour une mise de pari (Bet)
class BetRequest(BaseModel):
    amount: float  # Montant misé
    numbers: list[int]  # Liste de numéros choisis par le joueur

class ManualDepositRequest(BaseModel):
    user_id: int
    amount: float
