import sys
import app
from data_model import Ruolo
from collections import namedtuple
from typing import Sequence

# 1. Definizione della struttura dati usata per configurare i menu
MenuItem = namedtuple('MenuItem', ['label', 'roles', 'action'])


# ==========================================
# DIALOGHI DI INPUT
# ==========================================

def dialog_login():
    """Gestisce l'inserimento delle credenziali e avvia il menu dinamico."""
    while True:    
        print("\n--- LOGIN ---")
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        if not email or not password:
            print("\n[ERRORE] Tutti i campi sono obbligatori.")
            continue
            
        ruolo = app.login_spettatore(email, password)
        if ruolo:
            print(f"\n[SUCCESS] Login effettuato con successo!")
            print(f"Benvenuto {app.current_user.nome}!")
            
            # IMPORT LOCALE: Carichiamo app_menu qui dentro per evitare un import circolare,
            # dato che app_menu deve a sua volta importare textui per usare la classe Menu.
            import app_menu
            
            # Avviamo il menu principale passando il ruolo reale dell'utente
            app_menu.main_menu.show(ruolo)
            break
        else:
            print("\n[ERRORE] Credenziali errate. Riprova.")


def dialog_registrati():
    """Raccoglie i dati per creare un nuovo spettatore."""
    print("\n--- REGISTRAZIONE NUOVO SPETTATORE ---")
    
    nome = input("Nome: ").strip()
    cognome = input("Cognome: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    if not all([nome, cognome, email, password]):
        print("\n[ERRORE] Tutti i campi sono obbligatori per la registrazione.")
        return
        
    try:
        app.registra_spettatore(nome, cognome, email, password)
        print(f"\n[SUCCESS] Registrazione completata! Ora puoi effettuare il login.")
    except Exception as e:
        print(f"\n[ERRORE] Impossibile registrare l'utente: {e}")

class Menu():
    def __init__(self, menu_items: Sequence[MenuItem]):
        self._menu_items = menu_items

    def _get_input(self, max_choice):
        scelta = input("scelta: ")
        try:
            scelta = int(scelta)
            if scelta < 1 or scelta > max_choice:
                scelta = None
        except ValueError:
                scelta = None

        return scelta
    
    def _draw(self, visible_items):
        """Stampa le voci disponibili e l'uscita UNA SOLA VOLTA alla fine."""
        for nr, voce in enumerate(visible_items, 1):
            # Nota: Usiamo voce[0] o voce.label a seconda di come hai estratto la tupla.
            # Se visible_items contiene le namedtuple sane, voce.label è perfetto.
            print(f"{nr}-{voce[0]}") 
        
        print("esci (CTRL C)")

    def show(self, ruolo):
        """Mostra il menu e gestisce l'input."""
        # Se hai estratto le tuple come (label, action) nel filtro:
        visible_items = [(voce.label, voce.action) for voce in self._menu_items if ruolo in voce.roles]
        
        max_choice = len(visible_items)
        try:
            while True:
                self._draw(visible_items)

                opzione = self._get_input(max_choice) 
                
                if opzione:
                    self._call(visible_items[opzione - 1][1], ruolo)
        except KeyboardInterrupt:
            return 

    def _call(self, target, ruolo):
        if isinstance(target, Menu):
            target.show(ruolo)
        elif callable(target):
            target()