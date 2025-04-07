import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "").strip().strip('"')

# 👉 Vérifier si l'URL est correcte
print(f"Database URL: {DATABASE_URL}")  

# Créer le moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles SQLAlchemy
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
