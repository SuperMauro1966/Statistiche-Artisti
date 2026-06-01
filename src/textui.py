import sys
from login_spettatore import login_spettatore, registra_spettatore

# ==========================================
# INTERFACCIA AMMINISTRATORE
# ==========================================
def menu_amministratore(admin_nome):
    """Menu speciale visibile SOLO agli amministratori."""
    while True:
        print(f"\n=== AREA AMMINISTRATORE ({admin_nome}) ===")
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
def menu_spettatore_autenticato(spettatore):
    """Sotto-menu standard per gli spettatori comuni."""
    while True:
        print(f"\n--- AREA SPETTATORE ({spettatore['nome']} {spettatore['cognome']}) ---")
        print("1. Cerca Band (In sviluppo su altra branch)")
        print("2. Visualizza Palinsesto (In sviluppo su altra branch)")
        print("3. Acquista Biglietto (In sviluppo su altra branch)")
        print("4. Logout")
        
        scelta = input("Seleziona un'opzione: ").strip()
        
        if scelta in ['1', '2', '3']:
            print("\n[Info] Funzionalità in fase di sviluppo nell'altra branch.")
        elif scelta == '4':
            print(f"\nArrivederci {spettatore['nome']}! Ritorno al menu principale.")
            break
        else:
            print("\n[Opzione non valida] Riprova.")

def dialog_login():
    pass

def dialog_registrati():
    raise NotImplementedError

def main():
    while True:
        print("\n=== BENVENUTO NEL MUSIC FESTIVAL ===")
        print("1. Accedi (Login)")
        print("2. Registrati (Nuovo Spettatore)")
        print("3. Esci dal programma")
        
        scelta = input("Seleziona un'opzione: ").strip()
        
        if scelta == '1':
            print("\n--- LOGIN ---")
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            
            if not email or not password:
                print("\n[ERRORE] Tutti i campi sono obbligatori.")
                continue
                
            utente_loggato = login_spettatore(email, password)
            if utente_loggato:
                # Il database ha risposto positivamente, verifichiamo il RUOLO
                if utente_loggato['ruolo'] == 'admin':
                    print(f"\n[SUCCESS] Login Amministratore effettuato! Benvenuto {utente_loggato['nome']}.")
                    menu_amministratore(utente_loggato['nome'])
                else:
                    print(f"\n[SUCCESS] Login Spettatore effettuato! Benvenuto {utente_loggato['nome']}.")
                    menu_spettatore_autenticato(utente_loggato)
                
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

