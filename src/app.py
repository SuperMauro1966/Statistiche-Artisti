from enum import Enum
from pathlib import Path
from datetime import datetime
import random
import string
import logging
from functools import wraps

import bcrypt

import db  
from data_model import User, Ruolo

logger = logging.getLogger(__name__)

def log_function(logger):
    def helper(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            logger.info(f"chiamata {f.__name__} ")
            logger.info(f"{args}, {kwargs}")
            res = f(*args, **kwargs)
            logger.info(f"uscita da {f.__name__}")
            return res
        return wrapper
    return helper

class AppException(Exception):
    ...

class AppRegUtente(AppException):
    ...

class AppConfigOption(AppException):
    ...

class AppBigliettoException(AppException):
    ...


current_user = None

@log_function(logger)
def start(config_option):
    db_config = config_option.get("database")
    if db_config is None:
        raise AppConfigOption("Errore: chiave database mancante")
    db.start_db(db_config)
#equivale a start = log_function(logger)(start)   
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
    if current_user is None:
        raise AppException("Errore: Devi essere loggato per acquistare un biglietto.")
    
    posti_disponibili = db.get_posti_rimanenti_settore(id_settore)
    if posti_disponibili is None:
        raise AppBigliettoException("Settore sconosciuto")

    if posti_disponibili.rimanenti < 1:
        raise AppBigliettoException("Posti esauriti")
    
    concerto = db.get_concerto_by_id(id_concerto)
    if concerto is None:
        raise AppBigliettoException("Concerto non trovato")

    settore = db.get_settore_by_id(id_settore)
    if settore is None:
        raise AppBigliettoException("settore non trovato")

    codice_biglietto = genera_codice_biglietto()
    data_ora_acquisto = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     # Chiamata al database passando l'ID dell'utente corrente
    return db.inserisci_biglietto(codice_biglietto, current_user.id, settore.id_settore, concerto.id_concerto, concerto.data_concerto, settore.prezzo_biglietto, data_ora_acquisto)

def genera_codice_biglietto():
    caratteri = string.ascii_uppercase + string.digits
    codice_biglietto = "TICKET-" + "".join(random.choice(caratteri) for _ in range(8))
    return codice_biglietto

def cerca_band_per_nome(testo_ricerca):
    """
    Cerca le band che contengono la stringa di ricerca nel nome di arte.
    Ritorna una lista di dizionari con i dettagli della band e la lista dei componenti.
    """
    # Recuperiamo le band corrispondenti dal DB
    record_band = db.ricerca_band_db(testo_ricerca)
    
    risultato_strutturato = []
    
    for b in record_band:
        # Per ogni band trovata, recuperiamo i suoi componenti dal DB
        componenti_gruppo = db.get_componenti_by_band_id(b.id_band)
        
        # Uniamo le informazioni in una struttura dati comoda per la UI
        dati_band = {
            "id_band": b.id_band,
            "nome_arte": b.nome_arte,
            "genere_principale": b.genere_principale,
            "biografia": b.biografia,
            "sito_web": b.sito_web,
            "link_instagram": b.link_instagram,
            "link_tiktok": b.link_tiktok,
            "componenti": componenti_gruppo  # Questa sarà una lista di NamedTuple dal database
        }
        risultato_strutturato.append(dati_band)
        
    return risultato_strutturato