from pydantic import BaseModel
from typing import Literal
from decimal import Decimal

# Schéma pour l'inscription
class UserCreate(BaseModel):
    username: str
    password: str

# Schéma pour afficher un utilisateur
class UserResponse(BaseModel):
    id: int
    username: str
    balance: Decimal  # Utilisation de Decimal pour la balance

    class Config:
        from_attributes = True
        orm_mode = True  # Cela permet de convertir les objets ORM en modèles Pydantic

# Schéma pour les transactions
class TransactionCreate(BaseModel):
    amount: float
    transaction_type: Literal["deposit", "withdrawal"]  # Limitation des types possibles

# Schéma pour la connexion de l'utilisateur
class UserLogin(BaseModel):
    username: str
    password: str
