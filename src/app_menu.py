import ui
import app

from data_model import Ruolo

__all__ = ["main_login", "main_menu"]

# costruisco il menu di login
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

# costruisco menu principale
menu_principale_data = [
    # --- VOCI CONDIVISE (Visibili sia a Spettatore che ad Amministratore) ---
    ui.MenuItem(
        "Cerca Band ",
        {Ruolo.SPETTATORE, Ruolo.AMMINISTRATORE}, 
        lambda :  NotImplementedError
    ),
    ui.MenuItem(
        "Visualizza Palinsesto ",
        {Ruolo.SPETTATORE, Ruolo.AMMINISTRATORE}, 
        lambda :  NotImplementedError
    ),
    ui.MenuItem(
        "Acquista Biglietto ",
        {Ruolo.SPETTATORE, Ruolo.AMMINISTRATORE}, 
        ui.dialog_acquista_biglietto
    ),
    ui.MenuItem(
        "Popola da json ",
        {Ruolo.SPETTATORE, Ruolo.AMMINISTRATORE}, 
        app.popola_dati_da_json
    ),
    # --- VOCI ESCLUSIVE (Visibili SOLO all'Amministratore) ---
    ui.MenuItem(
        "Visualizza Incassi Totali (Dati analisi)",
        {Ruolo.AMMINISTRATORE}, # <--- Solo l'admin lo vede
        lambda: print("\n[INCASSI] Calcolo degli incassi in corso... € 45.320,00")
    ),
    ui.MenuItem(
        "Gestisci Palinsesto Festival",
        {Ruolo.AMMINISTRATORE},
        lambda :  NotImplementedError
    ),
    ui.MenuItem(
        "Visualizza Statistiche Spettatori",
        {Ruolo.AMMINISTRATORE},
        lambda :  NotImplementedError
    )
]

main_menu = ui.Menu(menu_principale_data)

    