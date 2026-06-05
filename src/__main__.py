import os
import app
import db
import sys

from data_model import Ruolo
from app_menu import main_login

try:
    app.start()

except db.DbException as e:
    print("errore durante la connessione con il database")
    print(e)
    sys.exit(1)

main_login.show(Ruolo.GUEST)
app.stop()    
