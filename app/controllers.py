"""
Modulo controller che gestisce la logica tra model e view.
Responsabile per:
- Preparare i dati per le view
- Gestire le richieste dell'utente
- Coordinare model e view
"""

from flask import render_template, request
from app.models import recommend, provider_mapping, movies
import pandas as pd

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