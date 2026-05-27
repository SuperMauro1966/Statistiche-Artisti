import sys

# INTERFACCIA TERMINALE (CLI)
def menu_spettatore_autenticato(spettatore_nome):
    """Sotto-menu visibile solo dopo aver effettuato il login."""
    while True:
        print(f"\n--- AREA SPETTATORE ({spettatore_nome}) ---")
        print("1. Cerca Band (In sviluppo su altra branch)")
        print("2. Visualizza Palinsesto (In sviluppo su altra branch)")
        print("3. Acquista Biglietto (In sviluppo su altra branch)")
        print("4. Logout")
        
        scelta = input("Seleziona un'opzione: ").strip()
        
        if scelta in ['1', '2', '3']:
            print("\n[Info] Funzionalità in fase di sviluppo nell'altra branch.")
        elif scelta == '4':
            print(f"\nArrivederci! Ritorno al menu principale.")
            break
        else:
            print("\n[Opzione non valida] Riprova.")

def main():
    while True:
        print("\n=== BENVENUTO NEL MUSIC FESTIVAL ===")
        print("1. Accedi (Login Spettatore)")
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
                
            print("\n[INFO] Modulo Login integrato in arrivo dopo il merge.")
            print("[SUCCESS] Login effettuato (Simulazione)!")
            menu_spettatore_autenticato("Utente Test")
                
        elif scelta == '2':
            print("\n--- REGISTRAZIONE ---")
            nome = input("Nome: ").strip()
            cognome = input("Cognome: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            
            if not all([nome, cognome, email, password]):
                print("\n[ERRORE] Tutti i campi sono obbligatori per la registrazione.")
                continue
                
            print("\n[INFO] Modulo Registrazione integrato in arrivo dopo il merge.")
            
        elif scelta == '3':
            print("\nChiusura del programma. A presto!")
            sys.exit()
        else:
            print("\n[Opzione non valida] Riprova.")

if __name__ == "__main__":
    main()