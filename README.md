[deepseek_20250427_6b48c1.txt](https://github.com/user-attachments/files/19930622/deepseek_20250427_6b48c1.txt)# progetto_pss

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
'''
├── README.md
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-310.pyc
│   ├── app.cpython-310.pyc
│   ├── controller.cpython-310.pyc
│   ├── database.cpython-310.pyc
│   └── model.cpython-310.pyc
├── app.py
├── controller.py
├── data
│   ├── movie_dict.pkl
│   ├── movies.pkl
│   ├── providers_movies.csv
│   └── similarity.pkl
├── database.py
├── instance
├── model.py
├── requirements.txt
├── schema.sql
├── static
│   ├── css
│   │   └── style.css
│   └── js
│       ├── index.js
│       └── personal_area.js
├── templates
│   ├── index.html
│   ├── login.html
│   ├── personal_area.html
│   └── register.html
└── watchlist.db
'''

## Funzionalità Principali
1. Sistema di Raccomandazione
   - Ricerca un film e ottieni 5 suggerimenti basati su similarità
   - Filtra i risultati per piattaforma di streaming:

        - Netflix

        - Disney+

        - Amazon Prime

        - Apple TV

        - Tim Vision

2. Gestione Watchlist

    - Aggiungi/rimuovi film dalla tua lista personale

    - Svuota completamente la watchlist

    - Visualizza poster e link ai dettagli dei film

3. Autenticazione Utente

    - Registrazione nuovo account

    - Login/logout

    - Watchlist personale per ogni utente
