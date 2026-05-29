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
            user='root',         
            password='1234',     
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
    """Registra un nuovo spettatore nel database (ruolo default: spettatore)."""
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
    Ritorna un dizionario con i dati dell'utente (compreso il ruolo) se ha successo.
    """
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    # MODIFICA QUI: Abbiamo aggiunto 'ruolo' nella SELECT
    query = "SELECT id_spettatore, nome, cognome, email, ruolo, password_hash FROM spettatore WHERE email = %s"
    
    try:
        cursor.execute(query, (email,))
        utente = cursor.fetchone()
        
        if utente and check_password(password, utente['password_hash']):
            del utente['password_hash'] # Rimuoviamo l'hash per sicurezza
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