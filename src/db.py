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
    
    def start_db(self):
        try:
            self.connection = mariadb.connect(
            host='localhost',
            user='root',         
            password='1234',     
            database='MusicDB'
            )
        except (mariadb.DatabaseError, mariadb.InterfaceError) as e:
            raise ConnectionError(*e.args)
        except Exception as e: 
            raise DbGeneric(*e.args) 
    
    def end_db(self):
        if self.connection:
            self.connection.close()

_connection = Conn()

start_db = _connection.start_db
end_db = _connection.end_db


def get_user_by_email(email):
    cursor = _connection.connection.cursor(named_tuple=True)
    query = "SELECT id_spettatore, nome, cognome, email, ruolo, password_hash FROM spettatore WHERE email = ?"

    cursor.execute(query, (email,))
    temp_user = cursor.fetchone()
    cursor.close() # Buona pratica chiudere il cursore dopo l'uso
    
    if not temp_user:
        return None
        
    return User(
        id_spettatore = temp_user.id_spettatore,
        nome = temp_user.nome,
        cognome = temp_user.cognome,
        email = temp_user.email,
        ruolo = Ruolo(temp_user.ruolo),
        password_hash = temp_user.password_hash
        )


def registra_spettatore(nome, cognome, email, password):
    """Registra un nuovo spettatore nel database (ruolo default: spettatore)."""
    # CORREZIONE: Usiamo la connessione reale dell'oggetto _connection, proprio come sopra
    if not _connection.connection:
        return False
    
    cursor = _connection.connection.cursor()
    
    # CORREZIONE: MariaDB con il connettore nativo usa '?' come segnaposto, non '%s'
    query = """
        INSERT INTO spettatore (nome, cognome, email, password_hash)
        VALUES (?, ?, ?, ?)
    """
    
    try:
        cursor.execute(query, (nome, cognome, email, password))
        _connection.connection.commit()
        print("\n[SUCCESS] Registrazione completata con successo!")
        return True
    except mariadb.Error as e: # CORREZIONE: Usiamo mariadb.Error invece del generico Error
        if e.errno == 1062:
            print("\n[ERRORE] Questa email è già registrata nel sistema.")
        else:
            print(f"\n[ERRORE] Impossibile registrare l'utente: {e}")
        return False
    finally:
        cursor.close()