import os
import app
import db
import sys

from data_model import Ruolo

default = 'textui'

if os.environ.get('ARTISTIUI', default)==default:
    import textui as ui
else:
    import gui as ui

menu_login_data = [
    ui.MenuItem(
        "Accedi (Login)",
        {Ruolo.GUEST}, 
        ui.dialog_login
    ),
    ui.MenuItem(
        "Registrati (Nuovo Spettatore)",
        {Ruolo.GUEST}, 
        ui.dialog_registrati
    )
]

try:
    app.start()

except db.DbException as e:
    print("errore durante la connessione con il database")
    print(e)
    sys.exit(1)

main_login = ui.Menu(menu_login_data)
main_login.show(Ruolo.GUEST)
app.stop()    
