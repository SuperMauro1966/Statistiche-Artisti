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
    
    def start(self, config):
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
    
    def end(self):
        if self.connection:
            self.connection.close()

    def routine_temp(self):
        """Popola tutte le tabelle del festival leggendo la struttura annidata del file JSON."""
        percorso_file = os.path.join(os.path.dirname(__file__), "data", "festival.json")
        
        try:
            with open(percorso_file, "r", encoding="utf-8") as f:
                struttura_json = json.load(f)
                
            # Entriamo nella radice del JSON
            festival_data = struttura_json["festival"]
                
            cursor = self.connection.cursor()
            
            # 1. Inserimento FESTIVAL (con IGNORE per evitare crash se già esistente)
            cursor.execute(
                "INSERT IGNORE INTO festival (nome, data_inizio, data_fine, luogo) VALUES (?, ?, ?, ?)",
                (festival_data["nome"], festival_data["data_inizio"], festival_data["data_fine"], festival_data["luogo"])
            )
            
            # Recuperiamo l'ID del festival. Se esisteva già (lastrowid == 0), lo cerchiamo con una SELECT
            id_festival = cursor.lastrowid
            if id_festival == 0 or id_festival is None:
                cursor.execute("SELECT id_festival FROM festival WHERE nome = ?", (festival_data["nome"],))
                res_fest = cursor.fetchone()
                id_festival = res_fest[0]
            
            # 2. Ciclo sui PALCHI
            for p in festival_data["palchi"]:
                cursor.execute(
                    "INSERT IGNORE INTO palco (festival, nome_palco, capienza_massima, posizione) VALUES (?, ?, ?, ?)",
                    (id_festival, p["nome_palco"], p["capienza_massima"], p["posizione"])
                )
                
                # Recuperiamo l'ID del palco corrente
                id_palco = cursor.lastrowid
                if id_palco == 0 or id_palco is None:
                    cursor.execute("SELECT id_palco FROM palco WHERE nome_palco = ? AND festival = ?", (p["nome_palco"], id_festival))
                    res_palco = cursor.fetchone()
                    id_palco = res_palco[0]
                
                # 3. Ciclo sui SETTORI (con .get per sicurezza)
                for s in p.get("settori", []):
                    cursor.execute(
                        "INSERT IGNORE INTO settore (palco, nome_settore, capienza_settore, prezzo_biglietto) VALUES (?, ?, ?, ?)",
                        (id_palco, s["nome_settore"], s["capienza_settore"], s["prezzo_biglietto"])
                    )
                    
                # 4. Ciclo sui CONCERTI (con .get per evitare crash su palchi vuoti)
                for con in p.get("concerti", []):
                    band_data = con["band"]
                    
                    # 5. Inserimento BAND
                    cursor.execute(
                        "INSERT IGNORE INTO band_artista (nome_arte, genere_principale, biografia, sito_web, link_instagram, link_tiktok) VALUES (?, ?, ?, ?, ?, ?)",
                        (band_data["nome_arte"], band_data["genere_principale"], band_data["biografia"], band_data["sito_web"], band_data["link_instagram"], band_data["link_tiktok"])
                    )
                    
                    # Recuperiamo l'ID della band
                    id_band = cursor.lastrowid
                    if id_band == 0 or id_band is None:
                        cursor.execute("SELECT id_band FROM band_artista WHERE nome_arte = ?", (band_data["nome_arte"],))
                        res_band = cursor.fetchone()
                        id_band = res_band[0]
                    
                    # 6. Ciclo sui COMPONENTI della band
                    for comp in band_data.get("componenti_band", []):
                        cursor.execute(
                            "INSERT IGNORE INTO componente_band (band, nome_completo, ruolo) VALUES (?, ?, ?)",
                            (id_band, comp["nome_completo"], comp["ruolo"])
                        )
                        
                    # 7. Inserimento effettivo del CONCERTO
                    cursor.execute(
                        "INSERT IGNORE INTO concerto (band, palco, data_concerto, ora_inizio, ora_fine) VALUES (?, ?, ?, ?, ?)",
                        (id_band, id_palco, con["data_concerto"], con["ora_inizio"], con["ora_fine"])
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



class PoolCursors():
    def inizialize(self, conn):
        self.conn = conn
        self.cursors = {}
    
    def execute(self, id_cursor, query = "", data = tuple(), named_tuple = True):
        if self.cursors.get(id_cursor) is None:
            if named_tuple:
                cursor = self.conn.cursor(named_tuple = True, binary = True)
            else:
                cursor = self.conn.cursor(dictionary = True, binary = True)

            self.cursors[id_cursor] = (cursor, query)
            cursor.execute(query, data)
        else:
            cursor, q = self.cursors[id_cursor]
            return cursor.execute(q, data)
            
        return cursor
    
    def close(self):
        for c, _ in self.cursors.values():
            c.close()
    
_pool_cursors = PoolCursors()

def start_db(config):
        _connection.start(config)
        _pool_cursors.inizialize(_connection.connection)


def end_db():
    _pool_cursors.close()
    _connection.end

def get_user_by_email(email):
    if not _connection.connection:
        return None
        
    #cursor = _connection.connection.cursor(named_tuple=True)
    query = "SELECT id_spettatore, nome, cognome, email, ruolo, password_hash FROM spettatore WHERE email = ?"

    #cursor.execute(query, (email,))
    cursor = _pool_cursors.execute("get user by email", query, (email,))
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

def insert_festival(nome, data_inizio, data_fine, luogo):
    cursor = _connection.connection.cursor()
    cursor.execute(
                "INSERT INTO festival (nome, data_inizio, data_fine, luogo) VALUES (?, ?, ?, ?)",
                (nome, data_inizio, data_fine, luogo)
            )
    id = cursor.lastrowid
    cursor.close()
    return id

def crea_festival_from_dict(data):
    _connection.connection.begin()
    rollback = True
    try:
        id_festival = insert_festival(data["nome"] ,data["data_inizio"], data["data_fine"], data["luogo"])

    except mariadb.DatabaseError as e:
        raise DbGeneric(*e.args)

    else:
        rollback = False
    finally:
        if rollback:
            _connection.connection.rollback()
        else:
            _connection.connection.commit()

def get_concerti_disponibili():
    """Ritorna la lista dei concerti con i relativi palchi associati."""
    if not _connection.connection:
        return []
    
    cursor = _connection.connection.cursor(named_tuple=True)
    
    query = """
        SELECT c.id_concerto, b.nome_arte AS band, c.palco, c.data_concerto, c.ora_inizio 
        FROM concerto c
        JOIN band_artista b ON c.band = b.id_band
        ORDER BY c.data_concerto, c.ora_inizio
    """
    cursor.execute(query)
    risultati = cursor.fetchall()
    cursor.close()
    return risultati

def get_settori_by_palco(nome_palco):
    """Ritorna i settori disponibili per un determinato palco con i relativi prezzi."""
    if not _connection.connection:
        return []
    
    cursor = _connection.connection.cursor(named_tuple=True)
    query = """
        SELECT id_settore, nome_settore, prezzo_biglietto 
        FROM settore 
        WHERE palco = ?
    """
    cursor.execute(query, (nome_palco,))
    risultati = cursor.fetchall()
    cursor.close()
    return risultati

def get_concerto_by_id(id_concerto):
    cursor = _connection.connection.cursor(named_tuple=True)
    cursor.execute("SELECT id_concerto, band, palco, data_concerto, ora_inizio, ora_fine FROM concerto WHERE id_concerto = ?", (id_concerto,))
    res_concerto = cursor.fetchone()
    cursor.close()
    return res_concerto

def get_settore_by_id(id_settore):
    cursor = _connection.connection.cursor(named_tuple=True)
    cursor.execute("SELECT id_settore, palco, nome_settore, capienza_settore, prezzo_biglietto FROM settore WHERE id_settore = ?", (id_settore,))
    res_settore = cursor.fetchone()
    cursor.close()
    return res_settore


def inserisci_biglietto(codice_biglietto, id_spettatore, id_settore, id_concerto, data_festival_scelta, prezzo_pagato, data_ora_acquisto):
    """Inserisce un nuovo biglietto nel database con tutti i campi obbligatori richiesti dallo schema."""
    if not _connection.connection:
        return False
    
    _connection.connection.begin()
    cursor = _connection.connection.cursor()
    
    try:
        query = """
            INSERT INTO biglietto (
                codice_biglietto, 
                spettatore, 
                settore, 
                concerto, 
                data_festival_scelta, 
                prezzo_pagato, 
                data_ora_acquisto
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            codice_biglietto, 
            id_spettatore, 
            id_settore, 
            id_concerto, 
            data_festival_scelta, 
            prezzo_pagato, 
            data_ora_acquisto
        ))
        
        _connection.connection.commit()
        return True
        
    except mariadb.Error as e:
        _connection.connection.rollback()
        raise DbGeneric(f"Errore durante l'acquisto del biglietto: {e}")
    finally:
        cursor.close()

def get_posti_rimanenti_settore(id_settore):
    cursor = _connection.connection.cursor(named_tuple=True)
    query = """
        SELECT (s.capienza_settore - COUNT(b.codice_biglietto)) AS rimanenti
        FROM settore AS s
        LEFT JOIN biglietto AS b ON s.id_settore = b.settore
        WHERE s.id_settore = ?
        GROUP BY s.id_settore, s.capienza_settore;
    """

    cursor.execute(query, (id_settore,))
    res_rimanenti = cursor.fetchone()
    cursor.close()

    return res_rimanenti

def ricerca_band_db(stringa_ricerca):
    """Esegue la query di ricerca parziale sulla tabella band_artista usando LIKE."""
    if not _connection.connection:
        return []

    cursor = _connection.connection.cursor(named_tuple=True)
    parametro_like = f"%{stringa_ricerca}%"
    
    query = """
        SELECT id_band, nome_arte, genere_principale, biografia, sito_web, link_instagram, link_tiktok 
        FROM band_artista 
        WHERE nome_arte LIKE ?
        ORDER BY nome_arte
    """
    
    cursor.execute(query, (parametro_like,))
    risultati = cursor.fetchall()
    cursor.close()
    return risultati

def get_componenti_by_band_id(id_band):
    """Recupera tutti i componenti associati all'ID di una determinata band."""
    if not _connection.connection:
        return []

    cursor = _connection.connection.cursor(named_tuple=True)
    query = """
        SELECT nome_completo, ruolo 
        FROM componente_band 
        WHERE band = ?
        ORDER BY nome_completo
    """
    
    cursor.execute(query, (id_band,))
    risultati = cursor.fetchall()
    cursor.close()
    return risultati

def get_incassi_totali():
    """Esegue la somma di tutti i prezzi dei biglietti venduti nel database."""
    if not _connection.connection:
        return 0.0
        
    cursor = _connection.connection.cursor()
    query = "SELECT SUM(prezzo_pagato) FROM biglietto"
    
    try:
        cursor.execute(query)
        risultato = cursor.fetchone()
        return risultato[0] if risultato[0] is not None else 0.0
    except mariadb.Error as e:
        raise DbGeneric(f"Errore nel calcolo degli incassi dal DB: {e}")
    finally:
        cursor.close()

def get_tutte_le_band():
    """Recupera l'elenco di tutte le band registrate (ID e Nome) per la selezione nella UI."""
    if not _connection.connection:
        return []
    cursor = _connection.connection.cursor(named_tuple=True)
    cursor.execute("SELECT id_band, nome_arte FROM band_artista ORDER BY nome_arte")
    risultati = cursor.fetchall()
    cursor.close()
    return risultati

def inserisci_nuovo_concerto(id_band, id_palco, data_concerto, ora_inizio, ora_fine):
    """Inserisce un nuovo concerto nella tabella 'concerto'."""
    if not _connection.connection:
        return False
        
    cursor = _connection.connection.cursor()
    query = """
        INSERT INTO concerto (band, palco, data_concerto, ora_inizio, ora_fine)
        VALUES (?, ?, ?, ?, ?)
    """
    try:
        cursor.execute(query, (id_band, id_palco, data_concerto, ora_inizio, ora_fine))
        _connection.connection.commit()
        return True
    except mariadb.Error as e:
        _connection.connection.rollback()
        raise DbGeneric(f"Errore durante l'inserimento del concerto nel DB: {e}")
    finally:
        cursor.close()

def get_statistiche_generali():
    """Recupera il conteggio totale degli utenti spettatori e dei biglietti acquistati."""
    if not _connection.connection:
        return {"totale_spettatori": 0, "totale_biglietti": 0}
        
    cursor = _connection.connection.cursor()
    
    try:
        query_spettatori = "SELECT COUNT(*) FROM spettatore WHERE ruolo = 1"
        cursor.execute(query_spettatori)
        totale_spettatori = cursor.fetchone()[0]
        
        query_biglietti = "SELECT COUNT(*) FROM biglietto"
        cursor.execute(query_biglietti)
        totale_biglietti = cursor.fetchone()[0]
        
        return {
            "totale_spettatori": totale_spettatori,
            "totale_biglietti": totale_biglietti
        }
    except mariadb.Error as e:
        raise DbGeneric(f"Errore nel recupero delle statistiche dal DB: {e}")
    finally:
        cursor.close()