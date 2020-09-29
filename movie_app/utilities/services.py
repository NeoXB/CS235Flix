from typing import Iterable
from movie_app.adapters.repository import AbstractRepository
from movie_app.domain.model import Movie
import random


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre.genre_name for genre in genres]
    return genre_names


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()
    if quantity >= movie_count:
        # Reduce quantity of ranks to generate if repo has insufficient number of movies.
        quantity = movie_count - 1

    # Pick distinct and random movies.
    random_ranks = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_rank(random_ranks)
    return movies_to_dict(movies)


# ============================================
# Functions to convert model entities to dicts
# ============================================
def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.rank,
        'title': movie.title,
        'release_year': movie.release_year,
        'description': movie.description
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
