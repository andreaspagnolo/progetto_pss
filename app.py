from flask import Flask, render_template, redirect, url_for, session, g
from controller import get_recommendations
from model import movies, fetch_poster_and_link
from database import get_db, init_db, close_db
import sqlite3
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.teardown_appcontext(close_db)

# Inizializza il database
init_db(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return get_recommendations()

@app.route('/add_to_watchlist/<movie_name>')
def add_to_watchlist(movie_name):
    movie_row = movies[movies['title'] == movie_name]
    if not movie_row.empty:
        movie_id = movie_row.iloc[0]['movie_id']
        try:
            movie_id = int(movie_id)
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "invalid_movie_id"})
        
        user_id = session.get('user_id', 'default_user')

        try:
            db = get_db()
            db.execute(
                "INSERT INTO watchlist (user_id, movie_name, movie_id) VALUES (?, ?, ?)",
                (user_id, movie_name, movie_id)
            )
            db.commit()
            return jsonify({"success": True, "message": "added"})
        except sqlite3.IntegrityError:
            return jsonify({"success": False, "message": "already_exists"})
    
    return jsonify({"success": False, "message": "movie_not_found"})

@app.route('/remove_from_watchlist/<movie_name>')
def remove_from_watchlist(movie_name):
    user_id = session.get('user_id', 'default_user')
    db = get_db()
    db.execute(
        "DELETE FROM watchlist WHERE user_id = ? AND movie_name = ?",
        (user_id, movie_name)
    )
    db.commit()
    return redirect(url_for('personal_area'))

@app.route('/personal_area')
def personal_area():
    user_id = session.get('user_id', 'default_user')
    db = get_db()
    
    # Esegui la query e converti le righe in dizionari
    watchlist_items = db.execute(
        "SELECT movie_name, movie_id FROM watchlist WHERE user_id = ?",
        (user_id,)
    ).fetchall()
    
    # Converti ogni riga SQLite in un dizionario
    watchlist_items = [dict(row) for row in watchlist_items]
    
    print("Watchlist items (converted to dict):", watchlist_items)  # Debug
    
    watchlist_movies = []
    for item in watchlist_items:
        print("Movie ID:", item['movie_id'], "| Name:", item['movie_name'])  # Debug
        poster, link = fetch_poster_and_link(item['movie_id'])
        watchlist_movies.append({
            'name': item['movie_name'],
            'poster': poster,
            'tmdb_link': link if link else "#"
        })
    
    return render_template('personal_area.html', watchlist=watchlist_movies)


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1")