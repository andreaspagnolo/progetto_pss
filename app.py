"""
Modulo principale dell'applicazione Flask.
Responsabile per:
- Configurazione dell'app
- Definizione delle route
- Gestione delle sessioni
- Autenticazione utenti
"""

from flask import Flask, render_template, redirect, url_for, session, g, request, flash
from app.controllers import get_recommendations
from app.models import movies, fetch_poster_and_link
from app.database import get_db, init_db, close_db, create_user, verify_user
import sqlite3
from flask import jsonify
import os

app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)
app.secret_key = os.urandom(24)
app.teardown_appcontext(close_db)

# Inizializza il database
init_db(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return get_recommendations()

# Route per il login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = verify_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

# Route per la registrazione
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if create_user(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists', 'error')
    
    return render_template('register.html')

# Route per il logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

# Route per aggiungere alla watchlist
@app.route('/add_to_watchlist/<movie_name>')
def add_to_watchlist(movie_name):
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "not_logged_in"})
    
    movie_row = movies[movies['title'] == movie_name]
    if not movie_row.empty:
        movie_id = movie_row.iloc[0]['movie_id']
        try:
            movie_id = int(movie_id)
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "invalid_movie_id"})
        
        try:
            db = get_db()
            db.execute(
                "INSERT INTO watchlist (user_id, movie_name, movie_id) VALUES (?, ?, ?)",
                (session['user_id'], movie_name, movie_id)
            )
            db.commit()
            return jsonify({"success": True, "message": "added"})
        except sqlite3.IntegrityError:
            return jsonify({"success": False, "message": "already_exists"})
    
    return jsonify({"success": False, "message": "movie_not_found"})

# Route per rimuovere dalla watchlist
@app.route('/remove_from_watchlist/<movie_name>')
def remove_from_watchlist(movie_name):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    db.execute(
        "DELETE FROM watchlist WHERE user_id = ? AND movie_name = ?",
        (session['user_id'], movie_name)
    )
    db.commit()
    return redirect(url_for('personal_area'))

# Route per l'area personale
@app.route('/personal_area')
def personal_area():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    watchlist_items = db.execute(
        "SELECT movie_name, movie_id FROM watchlist WHERE user_id = ?",
        (session['user_id'],)
    ).fetchall()
    
    watchlist_items = [dict(row) for row in watchlist_items]
    watchlist_movies = []
    
    for item in watchlist_items:
        poster, link = fetch_poster_and_link(item['movie_id'])
        watchlist_movies.append({
            'name': item['movie_name'],
            'poster': poster,
            'tmdb_link': link if link else "#"
        })
    
    return render_template('personal_area.html', watchlist=watchlist_movies)

# Route per svuotare la watchlist
@app.route('/clear_watchlist')
def clear_watchlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    db.execute(
        "DELETE FROM watchlist WHERE user_id = ?",
        (session['user_id'],)
    )
    db.commit()
    return redirect(url_for('personal_area'))

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1")