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
    """Richiama la logica di inserimento dati completa dal database."""
    try:
        # Chiamiamo direttamente la routine che fa TRUNCATE e poi i cicli for
        db._connection.routine_temp()
    except Exception as e:
        raise AppException(f"Errore durante il popolamento del database: {e}")
    
def ottieni_concerti():
    """Interfaccia tra UI e DB per recuperare i concerti."""
    return db.get_concerti_disponibili()

def ottieni_settori(nome_palco):
    """Interfaccia tra UI e DB per recuperare i settori di un palco."""
    return db.get_settori_by_palco(nome_palco)

def acquista_biglietto(id_settore, id_concerto):
    """
    Gestisce il processo di acquisto per l'utente attualmente loggato.
    Solleva un'eccezione se l'utente non è autenticato.
    """
    global current_user
    if current_user is None:
        raise AppException("Errore: Devi essere loggato per acquistare un biglietto.")
    
    # Chiamata al database passando l'ID dell'utente corrente
    return db.inserisci_biglietto(current_user.id, id_settore, id_concerto)