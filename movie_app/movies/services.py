from typing import List, Iterable
from movie_app.adapters.repository import AbstractRepository
from movie_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_rank: int, review_text: str, rating: int, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = Review(movie, review_text, rating)

    # Update the repository.
    repo.add_review(review)


def get_movie(movie_rank: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException
    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_first_movie()
    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):
    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_movie_ranks_for_genre(genre_name: str, repo: AbstractRepository):
    movie_ranks = repo.get_movie_ranks_for_genre(genre_name)
    return movie_ranks


def get_movies_by_rank(rank_list, repo: AbstractRepository):
    movies = repo.get_movies_by_rank(rank_list)
    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict


def get_reviews_for_movie(movie_rank, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException
    reviews = repo.get_reviews()
    review_list = []
    for review in reviews:
        if review.movie == movie:
            review_list.append(review)
    return reviews_to_dict(review_list)


# ============================================
# Functions to convert model entities to dicts
# ============================================
def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.rank,
        'title': movie.title,
        'release_year': movie.release_year,
        'description': movie.description,
        'director': director_to_dict(movie.director),
        'actors': actors_to_dict(movie.actors),
        'genres': genres_to_dict(movie.genres),
        'runtime_minutes': movie.runtime_minutes,
        'rating': movie.rating,
        'votes': movie.votes,
        'revenue': movie.revenue,
        'metascore': movie.metascore
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'movie_rank': review.movie.rank,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def director_to_dict(director: Director):
    director_dict = {
        'director_name': director.director_full_name
    }
    return director_dict


def directors_to_dict(directors: Iterable[Director]):
    return [director_to_dict(director) for director in directors]


def actor_to_dict(actor: Actor):
    actor_dict = {
        'actor_name': actor.actor_full_name
    }
    return actor_dict


def actors_to_dict(actors: Iterable[Actor]):
    return [actor_to_dict(actor) for actor in actors]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'genre_name': genre.genre_name,
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


# ============================================
# Functions to convert dicts to model entities
# ============================================
def dict_to_movie(dict):
    movie = Movie(dict.title, dict.release_year)
    movie.rank = dict.rank
    movie.description = dict.description
    movie.director = dict_to_director(dict.director)
    movie.actors = dict_to_actors(dict.actors)
    movie.genres = dict_to_genres(dict.genres)
    movie.runtime_minutes = dict.runtime_minutes
    movie.rating = dict.rating
    movie.votes = dict.votes
    movie.revenue = dict.revenue
    movie.metascore = dict.metascore
    return movie


def dict_to_director(dict):
    director = Director(dict.director_name)
    return director


def dict_to_actors(dict_list):
    actor_list = []
    for dict in dict_list:
        actor_list.append(Actor(dict.actor_name))
    return actor_list


def dict_to_genres(dict_list):
    genre_list = []
    for dict in dict_list:
        genre_list.append(Genre(dict.genre_name))
    return genre_list
