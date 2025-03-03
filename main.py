from fastapi import FastAPI
from database import Base, engine
from routes import auth, transactions, game  # Importation des routes

app = FastAPI()

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Inclure les routes
app.include_router(auth.router, prefix="/auth", tags=["Authentification"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(game.router, prefix="/game", tags=["Jeu"])  # Route pour le jeu

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur votre application de jeu !"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)  # Ajout de reload=True
