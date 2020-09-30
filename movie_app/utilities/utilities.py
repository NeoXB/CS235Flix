from flask import Blueprint, request, render_template, redirect, url_for, session
import movie_app.adapters.repository as repo
import movie_app.utilities.services as services

# Configure Blueprint.
utilities_blueprint = Blueprint('utilities_bp', __name__)


def get_genres_and_urls():
    genre_names = services.get_genre_names(repo.repo_instance)
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('movies_bp.movies_by_genre', genre=genre_name)
    return genre_urls


def get_featured_movies(quantity=3):
    movies = services.get_random_movies(quantity, repo.repo_instance)
    for movie in movies:
        movie['hyperlink'] = url_for('movies_bp.movies_by_rank', rank=movie['rank'])
    return movies
