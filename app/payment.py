from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Transaction
from app.schemas import TransactionRequest
from app.auth import get_current_user
import requests

router = APIRouter()

# Route pour traiter les paiements
@router.post("/payment")
async def process_payment(request: TransactionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    import uuid
    API_KEY = "98515895867db39a16faa05.64120201"
    ID_SITE = "105890281"
    payment_url = "https://api-checkout.cinetpay.com/v2/payment"

    transaction_id = str(uuid.uuid4())

    payment_data = {
        "apikey": API_KEY,
        "site_id": ID_SITE,
        "transaction_id": transaction_id,
        "amount": str(request.amount),
        "currency": "XOF",
        "description": "Dépôt pour E.Bet",
        "customer_name": current_user.username,
        "customer_surname": "",
        "customer_email": current_user.email,
        "customer_phone_number": request.phone_number,
        "customer_address": "Adresse",
        "customer_city": "Ville",
        "customer_country": "CI",
        "customer_state": "Etat",
        "channels": "ALL",
        "notify_url": "https://ton-domaine.com/notify",  # Remplace par ton URL publique
        "return_url": "https://ton-domaine.com/success"
    }

    try:
        response = requests.post(payment_url, json=payment_data)
        response_data = response.json()

        if response_data.get("code") == "201":
            payment_link = response_data.get("data", {}).get("payment_url")
            if not payment_link:
                raise HTTPException(status_code=400, detail="Lien de paiement introuvable")

            transaction = Transaction(
                user_id=current_user.id,
                amount=request.amount,
                transaction_type="deposit",
                status="pending",  # en attente jusqu'à la notification
                transaction_id=transaction_id
            )
            db.add(transaction)
            db.commit()

            return {"message": "Redirection vers CinetPay", "payment_url": payment_link}
        else:
            raise HTTPException(status_code=400, detail="Échec du paiement")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du paiement : {str(e)}")

# Route pour récupérer l'historique des paiements
@router.get("/payments")
async def get_payments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payments = db.query(Transaction).filter(Transaction.user_id == current_user.id).order_by(Transaction.timestamp.desc()).all()
    
    return {
        "payments": [
            {
                "id": payment.id,
                "amount": payment.amount,
                "status": payment.status,
                "transaction_type": payment.transaction_type,
                "timestamp": payment.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
            for payment in payments
        ]
    }

# Route pour valider un paiement après notification (par exemple depuis CinetPay)
@router.post("/validate-payment")
async def validate_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        # Valider le paiement dans la base de données
        transaction = db.query(Transaction).filter(Transaction.id == payment_id).first()
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction non trouvée")
        
        # Mise à jour du statut de la transaction (ici, on considère qu'on le valide après réception de la notification)
        transaction.status = "completed"
        db.commit()

        # Mettre à jour le solde de l'utilisateur en fonction du montant de la transaction
        user = db.query(User).filter(User.id == transaction.user_id).first()
        user.balance += transaction.amount
        db.commit()

        return {"message": "Paiement validé et solde mis à jour"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la validation du paiement: {str(e)}")
