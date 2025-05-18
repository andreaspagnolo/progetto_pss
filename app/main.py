"""
Definizione dell'app Flask, registrazione delle route e configurazione generale.
"""

from flask import Flask
from app.controllers import (
    get_recommendations, handle_login, handle_register, handle_logout,
    add_movie_to_watchlist, remove_movie_from_watchlist, get_personal_area,
    clear_user_watchlist
)
from app.database import init_db, close_db
import os

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.secret_key = os.urandom(24)
    app.teardown_appcontext(close_db)

    # Inizializza il database
    init_db(app)

    # ROUTES
    @app.route('/', methods=['GET', 'POST'])
    def index():
        return get_recommendations()

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return handle_login()

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        return handle_register()

    @app.route('/logout')
    def logout():
        return handle_logout()

    @app.route('/add_to_watchlist/<movie_name>')
    def add_to_watchlist(movie_name):
        return add_movie_to_watchlist(movie_name)

    @app.route('/remove_from_watchlist/<movie_name>')
    def remove_from_watchlist(movie_name):
        return remove_movie_from_watchlist(movie_name)

    @app.route('/personal_area')
    def personal_area():
        return get_personal_area()

    @app.route('/clear_watchlist')
    def clear_watchlist():
        return clear_user_watchlist()

    return app