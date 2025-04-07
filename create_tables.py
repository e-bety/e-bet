from database import engine, Base
from models import User, Transaction, Bet

try:
    # Vérifier la connexion à PostgreSQL
    with engine.connect() as connection:
        print("Connexion réussie à la base de données PostgreSQL.")

    # Création des tables
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès !")

except Exception as e:
    print(f"Erreur lors de la connexion ou de la création des tables : {e}")
