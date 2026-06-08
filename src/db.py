import json
import os
import mariadb
from data_model import User, Ruolo

class DbException(Exception):
    ...

class DbConnectionError(DbException):
    pass

class DbGeneric(DbException):
    "errore generico"


class Conn():
    connection = None
    
    def start_db(self, config):
        try:
            self.connection = mariadb.connect(
                host=config["host"],
                user=config["user"],         
                password=config["password"],     
                database=config["database"]
            )
        except (mariadb.DatabaseError, mariadb.InterfaceError) as e:
            raise DbConnectionError(*e.args)
        except Exception as e: 
            raise DbGeneric(*e.args) 
    
    def end_db(self):
        if self.connection:
            self.connection.close()

    # --- NUOVA FUNZIONE DI POPOLAMENTO (SENZA USARE .GET) ---
    def popola_database_da_json(self):
        """Popola tutte le tabelle del festival leggendo il file JSON usando le parentesi quadre."""
        # Trova il percorso assoluto della cartella 'data' partendo dalla posizione di questo file
        percorso_file = os.path.join(os.path.dirname(__file__), "data", "festival.json")
        
        try:
            with open(percorso_file, "r", encoding="utf-8") as f:
                dati = json.load(f)
                
            cursor = self.connection.cursor()
            
            # 1. Inserimento FESTIVAL
            for f in dati["festival"]:
                cursor.execute(
                    "INSERT IGNORE INTO festival (nome, data_inizio, data_fine, luogo) VALUES (?, ?, ?, ?)",
                    (f["nome"], f["data_inizio"], f["data_fine"], f["luogo"])
                )
            
            # 2. Inserimento PALCHI
            for p in dati["palchi"]:
                cursor.execute(
                    "INSERT IGNORE INTO palco (festival, nome_palco, capienza_massima, posizione) VALUES (?, ?, ?, ?)",
                    (p["festival"], p["nome_palco"], p["capienza_massima"], p["posizione"])
                )
                
            # 3. Inserimento SETTORI
            for s in dati["settori"]:
                cursor.execute(
                    "INSERT IGNORE INTO settore (palco, nome_settore, capienza_settore, prezzo_biglietto) VALUES (?, ?, ?, ?)",
                    (s["palco"], s["nome_settore"], s["capienza_settore"], s["prezzo_biglietto"])
                )
                
            # 4. Inserimento BAND ARTISTI
            for b in dati["band_artisti"]:
                cursor.execute(
                    "INSERT IGNORE INTO band_artista (nome_arte, genere_principale, biografia, sito_web, link_instagram, link_tiktok) VALUES (?, ?, ?, ?, ?, ?)",
                    (b["nome_arte"], b["genere_principale"], b["biografia"], b["sito_web"], b["link_instagram"], b["link_tiktok"])
                )
                
            # 5. Inserimento COMPONENTI BAND
            for c in dati["componenti_band"]:
                cursor.execute(
                    "INSERT IGNORE INTO componente_band (band, nome_completo, ruolo) VALUES (?, ?, ?)",
                    (c["band"], c["nome_completo"], c["ruolo"])
                )
                
            # 6. Inserimento CONCERTI
            for con in dati["concerti"]:
                cursor.execute(
                    "INSERT IGNORE INTO concerto (band, palco, data_concerto, ora_inizio, ora_fine) VALUES (?, ?, ?, ?, ?)",
                    (con["band"], con["palco"], con["data_concerto"], con["ora_inizio"], con["ora_fine"])
                )
            
            self.connection.commit()
            cursor.close()
            print("[DATABASE] Popolamento tabelle festival completato correttamente.")
            
        except FileNotFoundError:
            raise DbGeneric(f"Errore: File JSON non trovato in {percorso_file}")
        except KeyError as e:
            raise DbGeneric(f"Errore: Chiave {e} mancante nella struttura del JSON di popolamento")
        except mariadb.Error as e:
            if self.connection:
                self.connection.rollback()
            raise DbGeneric(f"Errore del database durante il popolamento: {e}")


_connection = Conn()

start_db = _connection.start_db
end_db = _connection.end_db
# Esponiamo all'esterno la nuova funzione per l'utilizzo in app.py
popola_database_da_json = _connection.popola_database_da_json


def get_user_by_email(email):
    if not _connection.connection:
        return None
        
    cursor = _connection.connection.cursor(named_tuple=True)
    query = "SELECT id_spettatore, nome, cognome, email, ruolo, password_hash FROM spettatore WHERE email = ?"

    cursor.execute(query, (email,))
    temp_user = cursor.fetchone()
    cursor.close()
    
    if not temp_user:
        return None
        
    return User(
        id_spettatore = temp_user.id_spettatore,
        nome = temp_user.nome,
        cognome = temp_user.cognome,
        email = temp_user.email,
        ruolo = Ruolo(temp_user.ruolo), # Converte l'intero del DB nell'Enum Ruolo
        password_hash = temp_user.password_hash
    )


def registra_spettatore(nome, cognome, email, password_criptata):
    """Inserisce materialmente i dati già validati nel database."""
    if not _connection.connection:
        return False
    
    cursor = _connection.connection.cursor()
    query = """
        INSERT INTO spettatore (nome, cognome, email, password_hash)
        VALUES (?, ?, ?, ?)
    """
    
    try:
        cursor.execute(query, (nome, cognome, email, password_criptata))
        _connection.connection.commit()
        return True
    except mariadb.Error:
        return False
    finally:
        cursor.close()