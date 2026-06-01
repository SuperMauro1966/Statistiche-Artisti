
import bcrypt
import db  
from enum import Enum
from data_model import User



current_user = None

def start():
    db.start_db()

def stop():
    db.end_db()

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
    utente = db.get_user_by_email(email)

    if utente and check_password(password, utente.password_hash):
            global current_user
            current_user = utente
            return Ruolo(utente.ruolo)
    
    return None
    
