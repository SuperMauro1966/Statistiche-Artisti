import sys
import mysql.connector
from mysql.connector import Error
import bcrypt

# ==========================================
# 1. CONFIGURAZIONE DATABASE
# ==========================================
def get_connection():
    """Stabilisce e restituisce la connessione al database MusicDB."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',         # Modifica con il tuo utente MySQL
            password='1234', # Modifica con la tua password MySQL
            database='MusicDB'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"\n[ERRORE] Connessione al database fallita: {e}")
        return None


# ==========================================
# 2. LOGICA DI AUTENTICAZIONE (AUTH)
# ==========================================
def hash_password(password: str) -> str:
    """Genera un hash sicuro per la password utilizzando bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    """Verifica se la password inserita corrisponde all'hash salvato."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def registra_spettatore(nome, cognome, email, password):
    """Registra un nuovo spettatore nel database."""
    conn = get_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    
    query = """
        INSERT INTO spettatore (nome, cognome, email, password_hash)
        VALUES (%s, %s, %s, %s)
    """
    
    try:
        cursor.execute(query, (nome, cognome, email, pwd_hash))
        conn.commit()
        print("\n[SUCCESS] Registrazione completata con successo!")
        return True
    except Error as e:
        if e.errno == 1062:
            print("\n[ERRORE] Questa email è già registrata nel sistema.")
        else:
            print(f"\n[ERRORE] Impossibile registrare l'utente: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def login_spettatore(email, password):
    """
    Effettua il login dello spettatore.
    Ritorna un dizionario con i dati dell'utente se ha successo, altrimenti None.
    """
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id_spettatore, nome, cognome, email, password_hash FROM spettatore WHERE email = %s"
    
    try:
        cursor.execute(query, (email,))
        utente = cursor.fetchone()
        
        if utente and check_password(password, utente['password_hash']):
            del utente['password_hash'] # Sicurezza: rimuoviamo l'hash dalla sessione locale
            return utente
        else:
            print("\n[ERRORE] Email o Password errate.")
            return None
            
    except Error as e:
        print(f"\n[ERRORE] Errore durante il login: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


# ==========================================
# 3. INTERFACCIA TERMINALE (CLI)
# ==========================================
def menu_spettatore_autenticato(spettatore):
    """Sotto-menu visibile solo dopo aver effettuato il login."""
    while True:
        print(f"\n--- AREA SPETTATORE ({spettatore['nome']} {spettatore['cognome']}) ---")
        print("1. Cerca Band (In sviluppo su altra branch)")
        print("2. Visualizza Palinsesto (In sviluppo su altra branch)")
        print("3. Acquista Biglietto (In sviluppo su altra branch)")
        print("4. Logout")
        
        scelta = input("Seleziona un'opzione: ").strip()
        
        if scelta == '1' or scelta == '2' or scelta == '3':
            print("\n[Info] Funzionalità in fase di sviluppo nell'altra branch.")
        elif scelta == '4':
            print(f"\nArrivederci {spettatore['nome']}! Ritorno al menu principale.")
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
                
            utente_loggato = login_spettatore(email, password)
            if utente_loggato:
                print(f"\n[SUCCESS] Login effettuato! Benvenuto {utente_loggato['nome']}.")
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

if __name__ == "__main__":
    main()