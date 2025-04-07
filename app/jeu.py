from fastapi import APIRouter

router = APIRouter()

@router.get("/jouer")
def jouer():
    return {"message": "Bienvenue dans le jeu!"}
