import os
import app
import db
import sys

default = 'textui'

if os.environ.get('ARTISTIUI', default)==default:
    import textui as ui
else:
    import gui as ui

try:
    app.start()

except db.DbException as e:
    print("errore durante la connessione con il database")
    print(e)
    sys.exit(1)

ui.main()


app.stop()    
