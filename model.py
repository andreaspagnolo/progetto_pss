"""
Modulo principale per la logica di raccomandazione dei film.
Gestisce:
- Caricamento dei dati dei film e delle piattaforme
- Accesso all'API TMDb
- Algoritmo di raccomandazione
- Mappatura delle piattaforme di streaming
"""

import pandas as pd
import pickle
import requests

# Chiave API per TMDb (da spostare in configurazione in produzione)
API_KEY = '9aba39119c399b5f3985ab6825be0aff'

# Caricamento dati delle piattaforme di streaming da CSV
providers_movies_df = pd.read_csv('data/providers_movies.csv')

# Caricamento dati dei film e matrice di similarità
movies_dict = pickle.load(open('data/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('data/similarity.pkl', 'rb'))

# Mappatura dei nomi delle piattaforme ai loro ID
provider_mapping = {
    'Netflix': 8,
    'Disney+': 337,
    'Amazon Prime': 119,
    'Apple tv': 2,
    'Tim vision': 109
}

def fetch_poster_and_link(movie_id):
    """
    Recupera il poster e il link TMDB per un film dato il suo ID.
    
    Args:
        movie_id (int/str): L'ID del film su TMDb
        
    Returns:
        tuple: (url_poster, link_scheda) o (None, None) in caso di errore
    """
    # Verifica e conversione del movie_id
    if not isinstance(movie_id, int):
        try:
            movie_id = int(movie_id)
        except (ValueError, TypeError):
            return None, None
    
    try:
        # Richiesta all'API TMDb
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US")
        response.raise_for_status()
        data = response.json()
        
        # Costruzione URL poster e link
        poster_url = f"https://image.tmdb.org/t/p/w500/{data['poster_path']}" if data.get('poster_path') else None
        movie_link = f"https://www.themoviedb.org/movie/{movie_id}" if movie_id else None
        return poster_url, movie_link
    except requests.exceptions.RequestException as e:
        print(f"Errore nel recupero del poster e del link per il film ID {movie_id}: {e}")
        return None, None

def get_movies_by_providers_cached(provider_ids):
    """
    Filtra i film disponibili sulle piattaforme specificate.
    
    Args:
        provider_ids (list): Lista di ID delle piattaforme
        
    Returns:
        set: Insieme di ID film disponibili sulle piattaforme
    """
    if not provider_ids:
        return set()
    
    # Filtra il dataframe per le piattaforme selezionate
    filtered_df = providers_movies_df[
        providers_movies_df['Provider'].isin(
            [k for k, v in provider_mapping.items() if v in provider_ids]
        )
    ]
    return set(filtered_df['Movie ID'].unique())

def recommend(movie, provider_ids=None):
    """
    Genera raccomandazioni di film basate su similarità e piattaforme.
    
    Args:
        movie (str): Nome del film di riferimento
        provider_ids (list, optional): Lista di ID piattaforme per filtrare
        
    Returns:
        tuple: (nomi_film, poster_urls, links_tmdb)
    """
    # Trova l'indice del film nel dataset
    movie_index = movies[movies['title'] == movie].index[0]
    
    # Ottieni le distanze di similarità
    distances = similarity[movie_index]
    
    # Ordina i film per similarità (escludendo il film stesso)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:]
    
    # Filtra per piattaforma se specificato
    platform_movie_ids = get_movies_by_providers_cached(provider_ids) if provider_ids else set()
    
    # Preparazione risultati
    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_links = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        # Applica filtro piattaforma se necessario
        if not provider_ids or movie_id in platform_movie_ids:
            poster, link = fetch_poster_and_link(movie_id)
            if poster and link:
                recommended_movies.append(movies.iloc[i[0]].title)
                recommended_movies_posters.append(poster)
                recommended_movies_links.append(link)
                
                # Limita a 5 risultati
                if len(recommended_movies) == 5:
                    break

    return recommended_movies, recommended_movies_posters, recommended_movies_links