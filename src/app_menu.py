import ui

from data_model import Ruolo

__all__ = ["main_login"]

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

main_login = ui.Menu(menu_login_data)