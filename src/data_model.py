from enum import Enum

class Ruolo(Enum):
    GUEST = 0
    SPETTATORE = 1
    AMMINISTRATORE = 2
    

class User():
     def __init__(self, id_spettatore, nome, cognome, email, ruolo, password_hash):
        self.id = id_spettatore
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.ruolo = ruolo
        self.password_hash = password_hash

