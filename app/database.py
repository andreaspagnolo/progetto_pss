"""
Modulo per la gestione del database SQLite.
Responsabile per:
- Connessione al database
- Operazioni CRUD sugli utenti
- Gestione della watchlist
- Hash delle password
"""

import sqlite3
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash
import os

DATABASE = 'watchlist.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        # Crea le tabelle se non esistono
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie_name TEXT NOT NULL,
                movie_id INTEGER NOT NULL,
                UNIQUE(user_id, movie_name),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        ''')
        db.commit()

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_user(username, password):
    db = get_db()
    password_hash = generate_password_hash(password)
    try:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user_by_username(username):
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    return user

def verify_user(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None