
import os
import psycopg2
from pathlib import Path
import pandas as pd
import sqlalchemy



CUSTOMER_FOLDER = "../data/customer"
DB_CLIENT = os.getenv("DB_URL" or None)

def handle_csv(file_path: str, engine: sqlalchemy.engine.Engine, table: str):
    try:
        data = pd.read_csv(file_path)
        if data.empty:
            print(f"Error: file {file_path} is empty")
        else:
            data.to_sql(table, engine)
    except Exception as e:
        print(f"Error: {e}")







if __name__ == "__main__":
    main()





import os
import glob
import logging
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

DOSSIER_CSV = "/data/csv"
DOSSIER_TRAITES = "/data/csv/traites"
CONNECTION_STRING = os.environ["DATABASE_URL"]
SI_TABLE_EXISTE = "append"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def importer_csv(fichier: str, engine) -> bool:
    nom_table = Path(fichier).stem.lower().replace(" ", "_").replace("-", "_")
    try:
        df = pd.read_csv(fichier)
        if df.empty:
            logger.warning(f"Fichier vide, ignoré : {fichier}")
            return False

        df.to_sql(nom_table, engine, if_exists=SI_TABLE_EXISTE, index=False, chunksize=1000)
        logger.info(f"✓ {fichier} → table '{nom_table}' ({len(df)} lignes)")
        return True

    except Exception as e:
        logger.error(f"✗ Échec import {fichier} : {e}")
        return False


def deplacer_fichier_traite(fichier: str):
    os.makedirs(DOSSIER_TRAITES, exist_ok=True)
    destination = os.path.join(DOSSIER_TRAITES, os.path.basename(fichier))
    os.rename(fichier, destination)


def main():
    engine = create_engine(CONNECTION_STRING)
    fichiers_csv = glob.glob(os.path.join(DOSSIER_CSV, "*.csv"))

    if not fichiers_csv:
        logger.info("Aucun fichier CSV trouvé.")
        return

    logger.info(f"{len(fichiers_csv)} fichier(s) CSV trouvé(s).")
    reussis, echoues = 0, 0
    for fichier in fichiers_csv:
        if importer_csv(fichier, engine):
            deplacer_fichier_traite(fichier)
            reussis += 1
        else:
            echoues += 1

    logger.info(f"Terminé : {reussis} réussi(s), {echoues} échec(s).")