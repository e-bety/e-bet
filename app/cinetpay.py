from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import requests
import decimal
import uuid
import webbrowser

router = APIRouter()

@router.post("/notify")
async def notify_payment(request: Request):
    data = await request.json()
    print("Notification de CinetPay reçue :", data)
    return JSONResponse({"status": "OK", "message": "Notification traitée"})

API_KEY = "98515895867db39a16faa05.64120201"
ID_SITE = "105890281"

def process_payment(amount: decimal.Decimal):
    url = "https://api.cinetpay.com/v1/transactions"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "site_id": ID_SITE,
        "apikey": API_KEY,
        "amount": str(amount),
        "currency": "XOF",
        "transaction_id": str(uuid.uuid4()),
        "description": "Dépôt pour le jeu E.Bet"
        # Tu peux ajouter ici : "payment_method": "MOBILE_MONEY", si besoin
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        print("Réponse de CinetPay :", response_data)

        if response_data.get("code") == "201":
            payment_url = response_data.get("data", {}).get("payment_url")
            if payment_url:
                webbrowser.open(payment_url)
                return {"message": "Redirection vers CinetPay", "payment_url": payment_url}
            else:
                raise HTTPException(status_code=400, detail="URL de paiement introuvable")
        else:
            raise HTTPException(status_code=400, detail=response_data.get("message", "Échec de la transaction"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de serveur : {str(e)}")
