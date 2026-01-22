import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

# Charge les variables d'environnement
load_dotenv()

CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

creds = Credentials.from_service_account_file(
    CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.readonly"]   
)

client = gspread.authorize(creds)

# Test : ouvrir une feuille Google Sheets
sheet = client.open("BrightBooks Financials").sheet1
data = sheet.get_all_records()

print("Connexion OK ! Nombre de lignes :", len(data))
