import os
import json
import sys
from pathlib import Path
import logging

import app
import db

from data_model import Ruolo
from app_menu import main_login

# Inizializzazione del logger globale come richiesto dal tutor
logger = logging.getLogger()
logging.basicConfig(filename="statistiche_artisti.log", level=logging.INFO)

try:
    logger.info("tentativo lettura config.json")
    config_path = Path(__file__).parent / "data" / "config.json"
    with open(config_path) as f : 
        config = json.load(f)    

    logger.info("letto correttamente config.json")
    
    if not isinstance(config, dict):
        logger.debug("config.json non covertito correttamente in un dizionario")
        raise ValueError
    logger.debug("config.json letto correttamente")

except ValueError as e:
    print("file json non contenente dizionario dati")
    print(e)
    sys.exit(1)

except Exception as e:
    print("errore durante la lettura del file config.json")
    print(e)
    sys.exit(1)

try:
    app.start(config)
except app.AppConfigOption as e:
    print(e)
    sys.exit(1)

except db.DbException as e:
    print("errore durante la connessione con il database")
    print(e)
    sys.exit(1)

main_login.show(Ruolo.GUEST)
app.stop()