import app  # Importiamo app per usare la funzione di hashing se serve, o db per il salvataggio
import db   # Importiamo db per comunicare i dati a MariaDB

def mostra_menu_registrazione():
    """
    Gestisce l'interfaccia testuale per la registrazione di un nuovo spettatore.
    Raccoglie i dati dall'input utente e li invia al database.
    """
    print("\n" + "="*40)
    print("      REGISTRAZIONE NUOVO UTENTE")
    print("="*40)
    
    # Raccolta dei dati con rimozione di spazi vuoti accidentali (.strip())
    nome = input("Inserisci il tuo Nome: ").strip()
    cognome = input("Inserisci il tuo Cognome: ").strip()
    email = input("Inserisci la tua Email: ").strip()
    password = input("Inserisci la tua Password (minimo 6 caratteri): ").strip()
    
    # Validazione base: controlliamo che nessun campo sia stato lasciato vuoto
    if not all([nome, cognome, email, password]):
        print("\n[ERRORE] Tutti i campi sono obbligatori per la registrazione!")
        return False

    print("\n[Elaborazione] Creazione dell'account in corso...")
    
    # Chiamata alla funzione del database (che abbiamo definito nel file db.py)
    successo = db.registra_spettatore(nome, cognome, email, password)
    
    if successo:
        print("\n[INFO] Ora puoi effettuare il login con le tue credenziali.")
        return True
    else:
        print("\n[ERRORE] Registrazione non riuscita. Riprova con dati diversi.")
        return False

# Questo blocco serve a te (o al tutor) per testare il file da solo
if __name__ == "__main__":
    # Inizializziamo temporaneamente il DB per testare se il file funziona da solo
    print("[Test] Avvio connessione DB per test singolo...")
    db.start_db()
    
    # Lancio del menu
    mostra_menu_registrazione()
    
    # Chiusura del DB dopo il test
    db.end_db()