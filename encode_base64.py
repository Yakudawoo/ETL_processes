import json
import os
import base64

# Chemin du fichier JSON
CREDENTIALS_PATH = os.path.join("credentials", "urbanmart-481617-59f5cf72df2b.json")

# Vérification
if not os.path.exists(CREDENTIALS_PATH):
    raise FileNotFoundError(f"Credentials not found at: {CREDENTIALS_PATH}")

# Chargement du JSON (pour vérifier qu’il est valide)
with open(CREDENTIALS_PATH, "r") as f:
    credentials = json.load(f)

print("Credentials loaded successfully.")

# Encodage base64 du fichier JSON
with open(CREDENTIALS_PATH, "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

# Écriture dans encoded.txt
with open("encoded.txt", "w") as out:
    out.write(encoded)

print("Encoded credentials saved to encoded.txt")
