import os
import pandas as pd
import gspread
from dotenv import load_dotenv
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials

load_dotenv()
# ---------------------------
# 1. EXTRACTION GOOGLE SHEETS
# ---------------------------

CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

creds = Credentials.from_service_account_file(
    CREDENTIALS_PATH,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]
)

client = gspread.authorize(creds)
sheet = client.open("BrightBooks Financials").sheet1
data = sheet.get_all_records()

df = pd.DataFrame(data)
print("Extraction OK :", df.shape)

# 21 janvier 2026 : ajout d'une nouvelle fonctionnalité
# ---------------------------
# 1.b (NOUVEAU) - Ajouter une seconde source Google Sheets
# ---------------------------

# IMPORTANT : La seconde feuille doit être partagée avec le même service account
sheet_2023 = client.open("BrightBooks Financials 2023").sheet1
data_2023 = sheet_2023.get_all_records()

df_2023 = pd.DataFrame(data_2023)
print("Extraction source 2023 OK :", df_2023.shape)

# Vérification pédagogique : colonnes identiques ?
assert list(df.columns) == list(df_2023.columns), "Les colonnes sont différentes !"

# Fusion (append vertical)
df_final = pd.concat([df, df_2023], ignore_index=True)
print("Fusion multi-source OK :", df_final.shape)

# Le reste du script continue en remplaçant df → df_final
df = df_final

# ---------------------------
# 2. CHARGEMENT DANS POSTGRES RDS
# ---------------------------

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")


engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

df.to_sql("financials", engine, if_exists="replace", index=False)

print("✅ Données exportées dans PostgreSQL !")