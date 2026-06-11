import sys
import app
from data_model import Ruolo
from collections import namedtuple
from typing import Sequence

# 1. Definizione della struttura dati usata per configurare i menu
MenuItem = namedtuple('MenuItem', ['label', 'roles', 'action'])


# ==========================================
# DIALOGHI DI INPUT
# ==========================================

def dialog_login():
    """Gestisce l'inserimento delle credenziali e avvia il menu dinamico."""
    while True:    
        print("\n--- LOGIN ---")
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        if not email or not password:
            print("\n[ERRORE] Tutti i campi sono obbligatori.")
            continue
            
        ruolo = app.login_spettatore(email, password)
        if ruolo:
            print(f"\n[SUCCESS] Login effettuato con successo!")
            print(f"Benvenuto {app.current_user.nome}!")
            
            # IMPORT LOCALE: Carichiamo app_menu qui dentro per evitare un import circolare,
            # dato che app_menu deve a sua volta importare textui per usare la classe Menu.
            import app_menu
            
            # Avviamo il menu principale passando il ruolo reale dell'utente
            app_menu.main_menu.show(ruolo)
            break
        else:
            print("\n[ERRORE] Credenziali errate. Riprova.")


def dialog_registrati():
    """Raccoglie i dati per creare un nuovo spettatore."""
    print("\n--- REGISTRAZIONE NUOVO SPETTATORE ---")
    
    nome = input("Nome: ").strip()
    cognome = input("Cognome: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    if not all([nome, cognome, email, password]):
        print("\n[ERRORE] Tutti i campi sono obbligatori per la registrazione.")
        return
        
    try:
        app.registra_spettatore(nome, cognome, email, password)
        print(f"\n[SUCCESS] Registrazione completata! Ora puoi effettuare il login.")
    except Exception as e:
        print(f"\n[ERRORE] Impossibile registrare l'utente: {e}")

def dialog_cerca_band():
    """Interfaccia testuale per cercare una band e visualizzare i dettagli ed i componenti."""
    print("\n--- CERCA BAND ---")
    stringa_ricerca = input("Inserisci il nome (o parte del nome) della band: ").strip()
    
    if not stringa_ricerca:
        print("\n[ERRORE] Inserisci almeno un carattere per avviare la ricerca.")
        return

    try:
        band_trovate = app.cerca_band_per_nome(stringa_ricerca)
        
        if not band_trovate:
            print(f"\n[INFO] Nessuna band trovata corrispondente a '{stringa_ricerca}'.")
            return

        print(f"\nRisultati trovati ({len(band_trovate)}):")
        for idx, band in enumerate(band_trovate, 1):
            print(f"\n{idx}) === {band['nome_arte'].upper()} ({band['genere_principale']}) ===")
            print(f"   Biografia: {band['biografia']}")
            if band['sito_web']:      print(f"   Sito Web:  {band['sito_web']}")
            if band['link_instagram']: print(f"   Instagram: {band['link_instagram']}")
            if band['link_tiktok']:    print(f"   TikTok:    {band['link_tiktok']}")
            
            # Mostriamo l'elenco dei componenti associati a questa band
            if band['componenti']:
                print("   Componenti del gruppo:")
                for comp in band['componenti']:
                    print(f"     - {comp.nome_completo} ({comp.ruolo})")
            else:
                print("   Componenti: Informazione non disponibile per questo artista.")
                
        print("\n-------------------------------------------")

    except Exception as e:
        print(f"\n[ERRORE] Si è verificato un problema durante la ricerca: {e}")

def dialog_visualizza_palinsesto():
    """Interfaccia testuale per visualizzare il palinsesto completo dei concerti."""
    print("\n--- PALINSESTO FESTIVAL ---")
    
    try:
        concerti = app.ottieni_concerti()
        
        if not concerti:
            print("\n[INFO] Il palinsesto è vuoto. Non ci sono concerti in programma.")
            return

        print(f"\nProgrammazione concerti ({len(concerti)} eventi in totale):")
        print("-" * 60)
        
        data_corrente = None
        for c in concerti:
            # Raggruppiamo visivamente per data per renderlo più leggibile
            if c.data_concerto != data_corrente:
                data_corrente = c.data_concerto
                print(f"\n[DATA: {data_corrente}]")
                print("=" * 20)
            
            print(f"  > Ore {c.ora_inizio} | Band: {c.band.upper()}")
            print(f"    Palco: {c.palco}")
            print("-" * 40)
            
        print("\n-------------------------------------------")

    except Exception as e:
        print(f"\n[ERRORE] Impossibile recuperare il palinsesto: {e}")
        
def dialog_acquista_biglietto():
    """Interfaccia testuale guidata per la selezione e l'acquisto di un biglietto."""
    print("\n--- ACQUISTO BIGLIETTO ---")
    
    # 1. Selezione del Concerto
    concerti = app.ottieni_concerti()
    if not concerti:
        print("\n[INFO] Non ci sono concerti disponibili al momento.")
        return

    print("\nSeleziona il concerto:")
    for idx, c in enumerate(concerti, 1):
        print(f"{idx}) {c.band} - Il {c.data_concerto} alle {c.ora_inizio} (Palco: {c.palco})")
    
    scelta_c = input("Scelta numero concerto (o Invio per annullare): ").strip()
    if not scelta_c.isdigit() or int(scelta_c) < 1 or int(scelta_c) > len(concerti):
        print("[ANNULLATO] Selezione non valida.")
        return
    
    concerto_scelto = concerti[int(scelta_c) - 1]

    # 2. Selezione del Settore basato sul palco del concerto scelto
    settori = app.ottieni_settori(concerto_scelto.palco)
    if not settori:
        print("\n[ERRORE] Nessun settore configurato per questo palco.")
        return

    print(f"\nSettori disponibili per il palco '{concerto_scelto.palco}':")
    for idx, s in enumerate(settori, 1):
        print(f"{idx}) {s.nome_settore} - Prezzo: € {s.prezzo_biglietto:.2f}")
    
    scelta_s = input("Scelta numero settore (o Invio per annullare): ").strip()
    if not scelta_s.isdigit() or int(scelta_s) < 1 or int(scelta_s) > len(settori):
        print("[ANNULLATO] Selezione non valida.")
        return
    
    settore_scelto = settori[int(scelta_s) - 1]

    # 3. Conferma ed Esecuzione dell'acquisto
    conferma = input(f"\nConfermi l'acquisto per {concerto_scelto.band} nel settore {settore_scelto.nome_settore} a € {settore_scelto.prezzo_biglietto:.2f}? (s/n): ").strip().lower()
    
    if conferma == 's':
        try:
            # Passiamo l'id del settore e l'id del concerto (l'id utente viene preso in automatico dal modulo app)
            successo = app.acquista_biglietto(settore_scelto.id_settore, concerto_scelto.id_concerto)
            if successo:
                print("\n[SUCCESS] Biglietto acquistato con successo! Buon festival!")
            else:
                print("\n[ERRORE] Impossibile completare l'acquisto del biglietto.")
        except Exception as e:
            print(f"\n[ERRORE] Si è verificato un problema: {e}")
    else:
        print("\n[ANNULLATO] Acquisto annullato dall'utente.")
        
class Menu():
    def __init__(self, menu_items: Sequence[MenuItem]):
        self._menu_items = menu_items

    def _get_input(self, max_choice):
        scelta = input("scelta: ")
        try:
            scelta = int(scelta)
            if scelta < 1 or scelta > max_choice:
                scelta = None
        except ValueError:
                scelta = None

        return scelta
    
    def _draw(self, visible_items):
        """Stampa le voci disponibili e l'uscita UNA SOLA VOLTA alla fine."""
        for nr, voce in enumerate(visible_items, 1):
            # Nota: Usiamo voce[0] o voce.label a seconda di come hai estratto la tupla.
            # Se visible_items contiene le namedtuple sane, voce.label è perfetto.
            print(f"{nr}-{voce[0]}") 
        
        print("esci (CTRL C)")

    def show(self, ruolo):
        """Mostra il menu e gestisce l'input."""
        # Se hai estratto le tuple come (label, action) nel filtro:
        visible_items = [(voce.label, voce.action) for voce in self._menu_items if ruolo in voce.roles]
        
        max_choice = len(visible_items)
        try:
            while True:
                self._draw(visible_items)

                opzione = self._get_input(max_choice) 
                
                if opzione:
                    self._call(visible_items[opzione - 1][1], ruolo)
        except KeyboardInterrupt:
            return 

    def _call(self, target, ruolo):
        if isinstance(target, Menu):
            target.show(ruolo)
        elif callable(target):
            target()

def dialog_visualizza_incassi():
    """Interfaccia testuale per mostrare all'amministratore gli incassi totali."""
    print("\n--- ANALISI DATI: INCASSI FESTIVAL ---")
    print("[INCASSI] Calcolo degli incassi in corso...")
    
    try:
        totale = app.ottieni_incassi_totali()
        print("-" * 45)
        print(f"  RICAVO TOTALE BIGLIETTI:  € {totale:,.2f}".replace(",", "."))
        print("-" * 45)
    except Exception as e:
        print(f"\n[ERRORE] Impossibile recuperare i dati finanziari: {e}")