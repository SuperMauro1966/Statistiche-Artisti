import sys
import app
from data_model import Ruolo
from collections import namedtuple
from typing import Sequence
# ==========================================
# INTERFACCIA AMMINISTRATORE
# ==========================================
def menu_amministratore():
    """Menu speciale visibile SOLO agli amministratori."""
    while True:
        print(f"\n=== AREA AMMINISTRATORE ({app.current_user.nome}) ===")
        print("1. Visualizza Incassi Totali (Dati analisi)")
        print("2. Gestisci Palinsesto Festival")
        print("3. Visualizza Statistiche Spettatori")
        print("4. Logout")
        
        scelta = input("Seleziona un'opzione: ").strip()
        
        if scelta == '1':
            print("\n[INCASSI] Calcolo degli incassi totali in corso... € 45.320,00 (Dato letto da DB)")
        elif scelta in ['2', '3']:
            print("\n[Info] Funzionalità admin in fase di sviluppo.")
        elif scelta == '4':
            print(f"\nArrivederci Admin {admin_nome}! Ritorno al menu principale.")
            break
        else:
            print("\n[Opzione non valida] Riprova.")

# ==========================================
# INTERFACCIA SPETTATORE
# ==========================================
def menu_spettatore_autenticato():
    """Sotto-menu standard per gli spettatori comuni."""
    while True:
        print(f"\n--- AREA SPETTATORE ({app.current_user.nome} {app.current_user.cognome}) ---")
        print("1. Cerca Band (In sviluppo su altra branch)")
        print("2. Visualizza Palinsesto (In sviluppo su altra branch)")
        print("3. Acquista Biglietto (In sviluppo su altra branch)")
        print("4. Logout")
        
        scelta = input("Seleziona un'opzione: ").strip()
        
        if scelta in ['1', '2', '3']:
            print("\n[Info] Funzionalità in fase di sviluppo nell'altra branch.")
        elif scelta == '4':
            print(f"\nArrivederci {app.current_user.nome}! Ritorno al menu principale.")
            break
        else:
            print("\n[Opzione non valida] Riprova.")

def dialog_login():
        
    while True:    
        print("\n--- LOGIN ---")
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        if not email or not password:
            print("\n[ERRORE] Tutti i campi sono obbligatori.")
            continue
            
        ruolo = app.login_spettatore(email, password)
        match ruolo:
            case data_model.Ruolo.AMMINISTRATORE:
                print(f"\n[SUCCESS] Login Amministratore effettuato!")
                menu_amministratore()
                break
            case data_model.Ruolo.SPETTATORE:
                print(f"\n[SUCCESS] Login Spettatore effettuato! Benvenuto {app.current_user.nome}.")
                menu_spettatore_autenticato()
                break
            case _:
                print("Credenziali errate")

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
        
    # --- NUOVO PEZZO: Salvataggio nel database ---
    try:
        # Passiamo i dati raccolti alla funzione del modulo app
        app.registra_spettatore(nome, cognome, email, password)
        print(f"\n[SUCCESS] Registrazione completata! Ora puoi effettuare il login.")
    except Exception as e:
        print(f"\n[ERRORE] Impossibile registrare l'utente: {e}")

def main():
    while True:
        print("\n=== BENVENUTO NEL MUSIC FESTIVAL ===")
        print("1. Accedi (Login)")
        print("2. Registrati (Nuovo Spettatore)")
        print("3. Esci dal programma")
        
        scelta = input("Seleziona un'opzione: ").strip()
        
        if scelta == '1':
            dialog_login()
                
        elif scelta == '2':
            print("\n--- REGISTRAZIONE ---")
            nome = input("Nome: ").strip()
            cognome = input("Cognome: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            
            if not all([nome, cognome, email, password]):
                print("\n[ERRORE] Tutti i campi sono obbligatori per la registrazione.")
                continue
                
            registra_spettatore(nome, cognome, email, password)
            
        elif scelta == '3':
            print("\nChiusura del programma. A presto!")
            sys.exit()
        else:
            print("\n[Opzione non valida] Riprova.")

MenuItem = namedtuple('MenuItem', ['label', 'roles', 'action'])

menu_login = [
    MenuItem(
        "Accedi (Login)",
        {Ruolo.GUEST}, 
        dialog_login
    ),
    MenuItem(
        "Registrati (Nuovo Spettatore)",
        {Ruolo.GUEST}, 
        dialog_registrati
    )
]

class Menu():
    def __init__(self, menu_items: Sequence[MenuItem]):
        self._menu_items = menu_items

    def _get_input(self, visible_items):
        scelta = input("scelta: ")
        try:
            scelta = int(scelta)
            if scelta < 1 or scelta > len(visible_items):
                scelta = None
        except ValueError:
                scelta = None

    def _draw(self, visible_items):
        """Stampa le voci disponibili e l'uscita UNA SOLA VOLTA alla fine."""
        for nr, voce in enumerate(visible_items, 1):
            # Nota: Usiamo voce[0] o voce.label a seconda di come hai estratto la tupla.
            # Se visible_items contiene le namedtuple sane, voce.label è perfetto.
            print(f"{nr}-{voce[0]}") 
        
        # --- CORREZIONE: Questo print deve stare FUORI dal ciclo for (senza spazi iniziali extra) ---
        print("0-Uscita dal programma")

    def show(self, ruolo):
        """Mostra il menu e gestisce l'input."""
        # Se hai estratto le tuple come (label, action) nel filtro:
        visible_items = [(voce.label, voce.action) for voce in self._menu_items if ruolo in voce.roles]
        
        while True:
            self._draw(visible_items)
            
            # Usiamo il tuo metodo _get_input o un input diretto
            scelta = input("scelta: ").strip()
            
            # Se l'utente preme 0, gestiamo l'uscita pulita che ha chiesto il tutor
            if scelta == '0':
                print("\nChiusura del programma. A presto!")
                sys.exit()
                
            if scelta.isdigit() and 1 <= int(scelta) <= len(visible_items):
                indice = int(scelta) - 1
                # Eseguiamo l'azione (che è in posizione [1] nella tupla filtrata)
                azione = visible_items[indice][1]
                azione()
                break
            else:
                print("\n[Opzione non valida] Riprova.")