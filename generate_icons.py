from PIL import Image

# Charger l'image source
image = Image.open(r"C:\Users\MARSEH TONLA\jeu 1\e-bet-game\public\logo.png")  # Chemin absolu

# Générer les icônes
image.resize((192, 192)).save(r"C:\Users\MARSEH TONLA\jeu 1\e-bet-game\public\icon-192x192.png")
image.resize((512, 512)).save(r"C:\Users\MARSEH TONLA\jeu 1\e-bet-game\public\icon-512x512.png")

print("✅ Icônes générées avec succès ! Vérifie ton dossier.")
