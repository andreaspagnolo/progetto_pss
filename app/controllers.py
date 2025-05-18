"""
Modulo controller che gestisce la logica tra model e view.
Responsabile per:
- Preparare i dati per le view
- Gestire le richieste dell'utente
- Coordinare model e view
"""

from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app.models import recommend, provider_mapping, movies, fetch_poster_and_link
from app.database import get_db, create_user, verify_user
import sqlite3

def get_recommendations():
    """
    Gestisce la logica per ottenere e visualizzare le raccomandazioni.
    
    Returns:
        Response: Template renderizzato con i dati appropriati
    """
    # Lista di tutti i film disponibili
    available_movies = movies['title'].tolist()

    # Gestione richiesta POST (form submission)
    if request.method == 'POST':
        selected_movie_name = request.form.get('movie')
        selected_platforms = request.form.getlist('platforms')
        
        # Mappa i nomi delle piattaforme ai loro ID
        selected_provider_ids = [
            provider_mapping[platform] 
            for platform in selected_platforms 
            if platform in provider_mapping
        ]

        # Ottieni raccomandazioni
        names, posters, links = recommend(selected_movie_name, selected_provider_ids)

        return render_template(
            'index.html', 
            names=names, 
            posters=posters, 
            links=links, 
            selected_movie_name=selected_movie_name, 
            movies=available_movies, 
            selected_platforms=selected_platforms
        )
    
    # Caso GET (primo accesso)
    return render_template(
        'index.html', 
        names=None, 
        movies=available_movies, 
        selected_platforms=[]
    )

def handle_login():
    """
    Gestisce la logica di login degli utenti.
    
    Returns:
        Response: Redirect o template renderizzato
    """
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

def handle_register():
    """
    Gestisce la logica di registrazione degli utenti.
    
    Returns:
        Response: Redirect o template renderizzato
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if create_user(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists', 'error')
    
    return render_template('register.html')

def handle_logout():
    """
    Gestisce la logica di logout degli utenti.
    
    Returns:
        Response: Redirect alla pagina di login
    """
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

def add_movie_to_watchlist(movie_name):
    """
    Aggiunge un film alla watchlist dell'utente.
    
    Args:
        movie_name (str): Nome del film da aggiungere
        
    Returns:
        Response: JSON con risultato dell'operazione
    """
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

def remove_movie_from_watchlist(movie_name):
    """
    Rimuove un film dalla watchlist dell'utente.
    
    Args:
        movie_name (str): Nome del film da rimuovere
        
    Returns:
        Response: Redirect alla pagina dell'area personale
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    db.execute(
        "DELETE FROM watchlist WHERE user_id = ? AND movie_name = ?",
        (session['user_id'], movie_name)
    )
    db.commit()
    return redirect(url_for('personal_area'))

def get_personal_area():
    """
    Recupera e visualizza l'area personale dell'utente con la watchlist.
    
    Returns:
        Response: Template renderizzato con i dati della watchlist
    """
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

def clear_user_watchlist():
    """
    Svuota completamente la watchlist dell'utente.
    
    Returns:
        Response: Redirect alla pagina dell'area personale
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    db.execute(
        "DELETE FROM watchlist WHERE user_id = ?",
        (session['user_id'],)
    )
    db.commit()
    return redirect(url_for('personal_area'))