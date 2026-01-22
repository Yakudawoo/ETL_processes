from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    """Crée et renvoie un moteur SQLAlchemy connecté à PostgreSQL."""
    return create_engine(
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

def get_sales_by_year():
    """Retourne un DataFrame avec les ventes annuelles."""
    
    query = """
    SELECT 
        "Year",
        SUM(
            REPLACE(REPLACE("Jan", '$',''), ',', '')::bigint +
            REPLACE(REPLACE("Feb", '$',''), ',', '')::bigint +
            REPLACE(REPLACE("Mar", '$',''), ',', '')::bigint +
            REPLACE(REPLACE("Apr", '$',''), ',', '')::bigint +
            REPLACE(REPLACE("May", '$',''), ',', '')::bigint +
            REPLACE(REPLACE("Jun", '$',''), ',', '')::bigint +
            REPLACE(REPLACE("Jul", '$',''), ',', '')::bigint +
            REPLACE(REPLACE("Aug", '$',''), ',', '')::bigint +
            REPLACE(REPLACE("Sep", '$',''), ',', '')::bigint +
            REPLACE(REPLACE("Oct", '$',''), ',', '')::bigint +
            REPLACE(REPLACE("Nov", '$',''), ',', '')::bigint +
            REPLACE(REPLACE("Dec", '$',''), ',', '')::bigint
        ) AS sales
    FROM financials
    WHERE "Account" = 'Sales'
    GROUP BY "Year"
    ORDER BY "Year";
    """
    
    engine = get_engine()
    df = pd.read_sql(query, engine)
    return df


# Permet d’exécuter le script seul pour debug
if __name__ == "__main__":
    print(get_sales_by_year())
