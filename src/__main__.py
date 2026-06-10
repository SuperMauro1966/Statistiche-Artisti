import os
import json
import sys
from pathlib import Path

import app
import db

from data_model import Ruolo
from app_menu import main_login

try:
    config_path = Path(__file__).parent / "data" / "config.json"
    with open(config_path) as f : 
        config = json.load(f)    

    if not isinstance(config, dict):
        raise ValueError

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