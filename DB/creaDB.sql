-- primo passo: cancello tutte le tabelle del database dde presenti
-- drop table if exist [nome tabella]
-- secondo passo: prima creo la tabella padre di una relazione e poi quella figlia
-- create table if not exist [nome tabella]
USE MusicDB 

DROP TABLE IF EXISTS biglietto
DROP TABLE IF EXISTS concerto
DROP TABLE IF EXISTS componente_band
DROP TABLE IF EXISTS settore
DROP TABLE IF EXISTS palco
DROP TABLE IF EXISTS festival    
DROP TABLE IF EXISTS band_artista
DROP TABLE IF EXISTS spettatore

    
    
CREATE TABLE IF NOT EXISTS festival (
    id_festival INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    data_inizio DATE NOT NULL,
    data_fine DATE NOT NULL,
    luogo VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_festival)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS palco (
    id_palco INT AUTO_INCREMENT,
    festival INT NOT NULL,
    nome_palco VARCHAR(100) NOT NULL,
    capienza_massima INT NOT NULL,
    posizione VARCHAR(255),
    PRIMARY KEY (id_palco),
    FOREIGN KEY (festival) REFERENCES festival(id_festival)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS settore (
    id_settore INT AUTO_INCREMENT,
    palco INT NOT NULL,
    nome_settore VARCHAR(100) NOT NULL,
    capienza_settore INT NOT NULL,
    prezzo_biglietto DECIMAL(6,2) NOT NULL,
    PRIMARY KEY (id_settore),
    FOREIGN KEY (palco) REFERENCES palco(id_palco)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS band_artista (
    id_band INT AUTO_INCREMENT,
    nome_arte VARCHAR(150) NOT NULL,
    genere_principale VARCHAR(50) NOT NULL,
    biografia TEXT,
    sito_web VARCHAR(255),
    link_instagram VARCHAR(255),
    link_tiktok VARCHAR(255),
    PRIMARY KEY (id_band)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS componente_band (
    id_componente INT AUTO_INCREMENT,
    band INT NOT NULL,
    nome_completo VARCHAR(150) NOT NULL,
    ruolo VARCHAR(100),
    PRIMARY KEY (id_componente),
    FOREIGN KEY (band) REFERENCES band_artista(id_band)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS concerto (
    id_concerto INT AUTO_INCREMENT,
    band INT NOT NULL,
    palco INT NOT NULL,
    data_concerto DATE NOT NULL,
    ora_inizio TIME NOT NULL,
    ora_fine TIME NOT NULL,
    PRIMARY KEY (id_concerto),
    FOREIGN KEY (band) REFERENCES band_artista(id_band),
    FOREIGN KEY (palco) REFERENCES palco(id_palco)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS spettatore (
    id_spettatore INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cognome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_spettatore),
    UNIQUE KEY unique_email (email)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS biglietto (
    codice_biglietto VARCHAR(50) NOT NULL,
    spettatore INT NOT NULL,
    settore INT NOT NULL,
    concerto INT NOT NULL,
    data_festival_scelta DATE NOT NULL,
    prezzo_pagato DECIMAL(6,2) NOT NULL,
    data_ora_acquisto DATETIME NOT NULL,
    PRIMARY KEY (codice_biglietto),
    FOREIGN KEY (spettatore) REFERENCES spettatore(id_spettatore),
    FOREIGN KEY (settore) REFERENCES settore(id_settore),
    FOREIGN KEY (concerto) REFERENCES concerto(id_concerto) 
) ENGINE=InnoDB;
