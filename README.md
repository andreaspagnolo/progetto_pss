## Descrizione del Progetto
<img width="1423" alt="Screenshot 2025-04-28 alle 10 32 38" src="https://github.com/user-attachments/assets/befa0667-b81e-401e-b857-7d2f1f8895b1" />

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
```
.
├── README.md
├── __init__.py
├── app.py
├── controller.py
├── data
│   ├── movie_dict.pkl
│   ├── movies.pkl
│   ├── providers_movies.csv
│   └── similarity.pkl
├── database.py
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

```

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

    - Visualizza titolo poster e link ai dettagli dei film

3. Autenticazione Utente

    - Registrazione nuovo account

    - Login/logout

    - Watchlist personale per ogni utente

## Installazione e Avvio

### Prerequisiti
- Python 3.x
- Pip

### Setup

1. Clona repository git clone
```
https://github.com/tuo-repository/movie-recommender.git
cd movie-recommender
```
2. Crea e attiva un ambiente virtuale (opzionale ma consigliato)
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Installa le dipendenze
```
pip install -r requirements.txt
```
4. Avvia l'applicazione
```
python app.py
```
5. Apri nel browser
```
http://localhost:5000
```

## Configurazione
Per utilizzare l'API TMDb, assicurati di avere una chiave API valida nel file model.py:
```
API_KEY = 'tua_chiave_api_tmdb'
```
