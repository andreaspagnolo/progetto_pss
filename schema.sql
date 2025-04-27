/*
Schema del database SQLite per l'applicazione.
Contiene:
- Tabella utenti
- Tabella watchlist
*/


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    movie_name TEXT NOT NULL,
    movie_id INTEGER NOT NULL,
    UNIQUE(user_id, movie_name)
);