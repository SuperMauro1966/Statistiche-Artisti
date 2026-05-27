Aggiornamento
Vorremmo che il nostro utilizzatore (sia Spettatore che Amministratore) possa essere a conoscenza di più dati possibili riguardanti il festival, gestendo in modo accurato la logistica, i biglietti e le interazioni.
Il festival è caratterizzato da uno o più palchi, nei quali verranno svolti dei concerti (anche contermporaneamente ma su palchi diversi).

festival:
  data di inizio
  data di fine
  Luogo
  sequenza di concerti (palinsesto)
  Palchi

Un concerto è caratterizzato da:
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
  
I dati che caratterizzano una band/artista:
- Dati identificativi
    Nome
    Genere principale (es. Rock, Metal, Indie)
    Biografia
    Elenco componenti del gruppo(per le band)

Un settore del palco (zona) è caratterizzato da:
  Nome del settore (es. Pit Gold - Sotto il palco, Tribuna Numerata, Prato)
  Capienza massima del settore (es. Pit Gold: 500 posti)
  Prezzo/Tariffa del biglietto per quel settore

Un biglietto acquistato è caratterizzato da:
  Codice univoco del biglietto (Generato automaticamente)
  Account dello Spettatore collegato
  Giorno del festival selezionato
  Tariffa e Posizione scelta (Settore)
  Prezzo pagato
  Data e ora dell'acquisto

Uno spettatore è caratterizzato da:
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
      
    
