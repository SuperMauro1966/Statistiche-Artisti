import os
import app

default = 'textui'

if os.environ.get('ARTISTIUI', default)==default:
    import textui as ui
else:
    import gui as ui

app.start()
ui.main()
app.stop()    
