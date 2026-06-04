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
        except :
            raise DbGeneric(*e.args) 
    
    def end_db(self):
        if self.connection:
            self.connection.close()

_connection = Conn()

start_db = _connection.start_db
end_db = _connection.end_db


def get_user_by_email(email):
    cursor = _connection.connection.cursor(named_tuple=True)
    # MODIFICA QUI: Abbiamo aggiunto 'ruolo' nella SELECT
    query = "SELECT id_spettatore, nome, cognome, email, ruolo, password_hash FROM spettatore WHERE email = ?"

    cursor.execute(query, (email,))
    temp_user = cursor.fetchone()
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