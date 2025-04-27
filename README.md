# progetto_pss

## Descrizione del Progetto
Movie Recommender è un'applicazione web che suggerisce film simili a quello selezionato dall'utente, filtrando i risultati in base alle piattaforme di streaming disponibili. Il sistema include:
- Un motore di raccomandazione basato su similarità tra film

- Gestione personalizzata della watchlist per ogni utente

- Autenticazione utente (login/registrazione)

- Integrazione con l'API TMDb per poster e informazioni sui film
    

## Tecnologie Utilizzate:
- Backend: Python con Flask

- Frontend: HTML5, CSS3, JavaScript

- Database: SQLite

- Librerie: Pandas, scikit-learn (per il modello di raccomandazione)

- API Esterna: The Movie Database (TMDb) API

## Struttura del Progetto (Pattern MVC)
movie-recommender/
│
├── static/
│   ├── css/
│   │   └── style.css          # Stili CSS
│   └── js/
│       ├── index.js           # Logica JS pagina principale
│       └── personal_area.js   # Logica JS area personale
│
├── templates/
│   ├── index.html             # Pagina principale
│   ├── login.html             # Pagina di login
│   ├── register.html          # Pagina di registrazione
│   └── personal_area.html     # Area personale/watchlist
│
├── data/                      # Dati e modelli precalcolati
│   ├── movie_dict.pkl         # Dizionario dei film
│   ├── similarity.pkl         # Matrice di similarità
│   └── providers_movies.csv   # Film per piattaforma
│
├── app.py                     # Applicazione principale (route)
├── controller.py              # Controller MVC
├── database.py                # Model per il database
├── model.py                   # Model per raccomandazioni
└── schema.sql                 # Schema del database

## Funzionalità Principali
1. Sistema di Raccomandazione
   - Ricerca un film e ottieni 5 suggerimenti basati su similarità
   - Filtra i risultati per piattaforma di streaming:

        - Netflix

        - Disney+

        - Amazon Prime

        - Apple TV

        - Tim Vision

3. Gestione Watchlist

    Aggiungi/rimuovi film dalla tua lista personale

    Svuota completamente la watchlist

    Visualizza poster e link ai dettagli dei film

4. Autenticazione Utente

    Registrazione nuovo account

    Login/logout

    Watchlist personale per ogni utente
