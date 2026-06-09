from enum import Enum
import json

import bcrypt
import db  

from pathlib import Path
from data_model import User, Ruolo

class AppException(Exception):
    ...

class AppRegUtente(AppException):
    pass

class AppConfigOption(AppException):
    ...

current_user = None

def start(config_option):
    db_config = config_option.get("database")
    if db_config is None:
        raise AppConfigOption("Errore: chiave database mancante")
    db.start_db(db_config)
    
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
    
def registra_spettatore(nome, cognome, email, password):
    if len(password) < 6:
        raise AppRegUtente(msg="[ERRORE VALIDAZIONE] La password deve contenere almeno 6 caratteri.")

    utente_esistente = db.get_user_by_email(email)
    if utente_esistente is not None:
        raise AppRegUtente(msg="\n[ERRORE VALIDAZIONE] Questa email è già registrata nel sistema.")
    
    # 1. Cifriamo la password con la funzione già presente in app.py
    password_criptata = hash_password(password)
    
    # 2. Chiamiamo la funzione di db.py usando il suo nome reale

    return db.registra_spettatore(nome, cognome, email, password_criptata)

def popola_dati_da_json():
    """Richiama la logica di inserimento dati dal database."""
    festival_path = Path(__file__).parent / "data" / "festival.json"
    try:
        with open(festival_path) as f : 
            festival = json.load(f)    
    except Exception as e:
        raise AppException("Errore nell'apertura/conversione file json")

    if not isinstance(festival, dict):
        raise ValueError("Impossibile aprire file festival.json")
    

    festival_data = festival.get("festival")

    if festival_data is None:
        raise ValueError("Chiave festival mancante")
    
    db.crea_festival_from_dict(festival_data)
    