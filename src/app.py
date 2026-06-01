
import bcrypt
import db  

def start():

    db.start_db()



def hash_password(password: str) -> str:
    """Genera un hash sicuro per la password utilizzando bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    """Verifica se la password inserita corrisponde all'hash salvato."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

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