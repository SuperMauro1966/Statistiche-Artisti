# **HUB MUSICALE (MusicDB): Analisi Approfondita del Database**

## **1\. Analisi Strutturale: I Tre Livelli di Dati**

L'architettura di MusicDB è concepita per essere a conoscenza dei dati degli artisti (cantanti). Ci saranno dati fissi (biografie, album), relazioni industriali (featuring, generi multipli) e flussi di dati sempre aggiornati (metriche di streaming da API).

### **A. Tabelle Anagrafiche e di Catalogo (I Dati Nucleo)**

* **`Artisti`**, **`Album`**, **`Canzoni`**, **`Generi`**  
* **Caratteristiche:** Custodiscono le informazioni strutturali della musica che non cambiano frequentemente.  
* **Ottimizzazione chiave:** Le tabelle `Artisti` e `Canzoni` implementano i campi `genius_id` con il vincolo `UNIQUE`. Questa scelta è fondamentale per l'interazione con Python: permette allo script di sincronizzazione di usare la logica di **Upsert** (`ON DUPLICATE KEY UPDATE`), garantendo che l'automazione possa aggiornare i record esistenti senza mai generare duplicati nell'anagrafica.

  ### **B. Tabelle di Relazione (Il Tessuto Connettivo)**

* **`Artisti_Canzoni`** e **`Artisti_Generi`**  
* **Caratteristiche:** Risolvono le relazioni **Molti-a-Molti** insite nel mercato discografico moderno.  
* **Ottimizzazione chiave:** Nella tabella `Artisti_Canzoni`, la chiave primaria è composta: `PRIMARY KEY (id_artista, id_canzone, tipo_contributo)`. Questa tripla combinazione permette di mappare scenari complessi (es. un artista che è sia produttore che featuring nello stesso brano) impedendo anomalie di ridondanza. L'integrità è protetta da vincoli `ON DELETE CASCADE`: se un artista viene rimosso, le sue collaborazioni svaniscono automaticamente per evitare record orfani.

  ### **C. Tabelle Transazionali e Storiche (La Cronologia Dinamica)**

* **`Metriche_Artisti`**, **`Metriche_Canzoni`**, **`Certificazioni`**  
* **Caratteristiche:** Registrano le fluttuazioni di mercato del comparto musicale (ascolti, views, premi).  
* **Ottimizzazione chiave:** L'uso del tipo di dato `BIGINT` per `ascolti_spotify` nella tabella `Metriche_Canzoni` previene il crash del database (Buffer Overflow) sopra i 2,1 miliardi di riproduzioni, inevitabile con i grandi successi internazionali. La strutturazione a "stack" (una riga nuova per ogni giorno di rilevazione) trasforma il DB in un archivio storico cronologico, ideale per l'analisi dei trend.

  ## **2\. Analisi delle Relazioni e Flussi di Navigazione**

L'alberatura del database permette a Python e Flask di navigare i dati in modo pulito ed efficiente:

* \[Album\] 1 ─── N \[Canzoni\]  
* \[Artisti\] N ─── N \[Canzoni\]  \---\> Risolta con Giunzione \[Artisti\_Canzoni\]  
* \[Artisti\] N ─── N \[Generi\]   \---\> Risolta con Giunzione \[Artisti\_Generi\]  
* \[Artisti\] 1 ─── N \[Metriche\_Artisti\]  
* \[Canzoni\] 1 ─── N \[Metriche\_Canzoni\]  
* \[Canzoni\] 1 ─── N \[Certificazioni\]  
    
* **Relazione Album \- Canzoni (1 a Molti con tolleranza `NULL`):** Gestita tramite `id_album INT` dentro `Canzoni`. Il vincolo `ON DELETE SET NULL` è una scelta di business: se un album viene rimosso dalle piattaforme, le canzoni rimangono memorizzate nel sistema come singoli (l'album diventa semplicemente `NULL`), preservando il patrimonio artistico del database.  
* **Disaccoppiamento delle Metriche:** Isolare le metriche dai dati anagrafici fa sì che lo script Python possa scrivere continuamente milioni di dati di ascolto giornalieri senza mai bloccare (in gergo *table locking*) l'interfaccia HTML di Flask che gli utenti usano per leggere le biografie degli artisti.


# Nuova Sezione
Vorremmo che il nostro utilizzatore possa essere a conoscenza di più dati possibili riguardanti un certo artista.
i dati che caratterizzano l'artista:


-dati anagrafici 
    nome
    cognome
    nome d'arte
    data di nascita
    luogo di nascita
    data di morte


-biografia


-discografia                                
    album prodotti


un album prodotto è caratterizzato da:
  titolo
  data di rilascio
  una sequenza di canzoni
  etichetta discografica
  numero traccia --> canzone

una canzone è caratterizzata da:
  un titolo
  una durata
  elenco dei collaboratori
  elenco dei video associati
  testo ---> numero visualizzazioni
  genere

i collaboratori di distinguono in:
  artista principale
  elenco artisti secondari (featured)
  parolieri
  elenco produttori


il programma deve poter visualizzare:
  -ascoltatori mensili dell'artista
  -10 canzoni più ascoltate dell'artista

certificazioni:
  premi
  dischi d'oro/argento/platino/diamante
  copie vendute

le copie vendute possono essere associate sia ad un singolo che ad un intero album, in relazione alle copie vendute.

le copie vendute sono generate partendo da due dati: 
  vendite fisiche
  ascolti digitali

fonti dati esterne:
  spotify
  genius
    biografia
    link video youtube della canzone
    data d'uscita
    singolo o numero traccia-->album



# Aggiornamento
Vorremmo che il nostro utilizzatore (sia Spettatore che Amministratore) possa essere a conoscenza di più dati possibili riguardanti il festival, gestendo in modo accurato la logistica, i biglietti e le interazioni.
Il festival è caratterizzato da uno o più palchi, nei quali verranno svolti dei concerti (anche contermporaneamente ma su palchi diversi).

festival:
  data di inizio
  data di fine
  palchi
  sequenza di concerti (palinsesto)

I dati che caratterizzano una band/artista:
- Dati identificativi
    Nome band / artista
    Genere principale (es. Rock, Metal, Indie)
    Biografia locale
    Elenco componenti del gruppo
- Contatti e Social
    Link al sito web ufficiale
    Link ai profili social (Instagram, TikTok)


Un concerto/esibizione è caratterizzato da:
  Band assegnata
  data (es. Venerdì, Sabato, Domenica)
  Ora inizio
  Ora fine
  Palco assegnato

Un palco è caratterizzato da:
  Nome palco (es. Palco Principale Arena, Palco Underground Tenda)
  Capienza massima di pubblico (limite di sicurezza)
  Posizione nell'area del festival
  Elenco dei settori associati

Un settore del palco (zona) è caratterizzato da:
  Nome della posizione (es. Pit Gold - Sotto il palco, Tribuna Numerata, Prato)
  Capienza massima del settore (es. Pit Gold: 500 posti)
  Prezzo/Tariffa del biglietto per quel settore

Un biglietto acquistato è caratterizzato da:
  Codice univoco del biglietto (Generato automaticamente)
  Account dello Spettatore collegato
  Giorno del festival selezionato
  Tariffa e Posizione scelta (Settore)
  Prezzo pagato
  Data e ora dell'acquisto

Un account spettatore è caratterizzato da:
  //ID_Spettatore
  Nome
  Cognome
  Email
  Password (per Autenticazione)
  Storico personale (Biglietti acquistati)

# Vincolo

Il programma deve poter visualizzare e controllare (Controlli automatici bloccanti):
  - Verifica Sovrapposizioni Band: Una band non può essere assegnata a due palchi diversi nello stesso momento.
  - Verifica Occupazione Palco: Sullo stesso palco non possono suonare due band contemporaneamente.
  - Controllo Disponibilità Posti (Sold Out): Quando un utente seleziona un settore, il sistema verifica in tempo reale che i biglietti venduti non abbiano raggiunto il limite massimo del settore. Se esauriti, blocca l'acquisto.

# Casi D'uso

Reportistica e Statistiche (Pannello Amministratore):
  - Report Incassi e Vendite: Totale dei soldi generati, suddivisi per settore e tariffa.
  - Statistiche Affollamento Palchi: Calcolo del pubblico previsto per ogni singolo giorno in base ai biglietti venduti (utile per la gestione della sicurezza).


Fonti di inserimento dati (Gestione locale e Interazioni):
  - Amministratore (Pannello di Controllo locale):
      Inserimento e modifica anagrafica Band
      Configurazione Palchi, Settori e relative capienze
      Gestione e modifica Tariffe/Prezzi
      Pianificazione del Calendario Orari dei concerti
  - Spettatore (Interfaccia Web / Menù del Sito):
      Registrazione e Login
      Ricerca Band per nome e filtri per Genere Musicale
      Visualizzazione del Palinsesto completo (Orari e Palchi)
      Acquisto online del biglietto (scelta giorno e posizione)
      
    