import os

default = 'textui'

if os.environ.get('ARTISTIUI', default)==default:
    from ui._textui import *
else:
    from ui._gui import *