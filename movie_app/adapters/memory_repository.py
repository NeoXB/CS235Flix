import os
from typing import List
from werkzeug.security import generate_password_hash
from movie_app.adapters.repository import AbstractRepository, RepositoryException
from movie_app.domain.model import Director, Genre, Actor, Movie, MovieFileCSVReader, Review, User, WatchList


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._directors = list()
        self._genres = list()
        self._actors = list()
        self._movies = list()
        self._movies_index = dict()
        self._reviews = list()
        self._users = list()
        self._all_watchlist = list()

    def add_director(self, director: Director):
        self._directors.append(director)

    def get_director(self, director_name) -> Director:
        return next(
            (director for director in self._directors if director.director_full_name == director_name), None)

    def add_genre(self, genre: Genre):
        self._genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self._genres

    def add_actor(self, actor: Actor):
        self._actors.append(actor)

    def get_actor(self, actor_name) -> Actor:
        return next((actor for actor in self._actors if actor.actor_full_name == actor_name), None)

    def add_movie(self, movie: Movie):
        self._movies.append(movie)
        self._movies_index[movie.rank] = movie

    def get_movie(self, rank: int) -> Movie:
        movie = None
        try:
            movie = self._movies_index[rank]
        except KeyError:
            pass  # Ignore exception and return None.
        return movie

    def get_number_of_movies(self):
        return len(self._movies)

    def get_first_movie(self) -> Movie:
        movie = None
        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self) -> Movie:
        movie = None
        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_movies_by_rank(self, rank_list):
        # Strip out any ranks in rank_list that don't represent Movie ranks in the repository.
        existing_ranks = [rank for rank in rank_list if rank in self._movies_index]

        # Fetch the Movies.
        movies = [self._movies_index[rank] for rank in existing_ranks]
        return movies

    def get_movie_ranks_for_genre(self, genre_name: str):
        # Linear search, to find the first occurrence of a Genre with the name genre_name.
        genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)

        # Retrieve the ranks of movies associated with the Genre.
        if genre is not None:
            movie_ranks = [movie.rank for movie in self._movies if genre in movie.genres]
        else:
            # No Genre with name genre_name. Return an empty list.
            movie_ranks = list()
        return movie_ranks

    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username: str) -> User:
        return next((user for user in self._users if user.user_name == username), None)

    def add_watchlist(self, watchlist: WatchList):
        self._all_watchlist.append(watchlist)

    def get_watchlist(self, user: User) -> List[WatchList]:
        all_watchlist = []
        for watchlist in self._all_watchlist:
            if watchlist.watchlist_owner == user:
                all_watchlist.append(watchlist)
        return all_watchlist


def load_data(data_path: str, repo: MemoryRepository):
    all_data = MovieFileCSVReader(os.path.join(data_path, 'Data1000Movies.csv'))
    all_data.read_csv_file()

    # load directors into repository.
    for director in all_data.dataset_of_directors:
        repo.add_director(director)

    # load genres into repository.
    for genre in all_data.dataset_of_genres:
        repo.add_genre(genre)

    # load actors into repository.
    for actor in all_data.dataset_of_actors:
        repo.add_actor(actor)

    # load movies into repository.
    for movie in all_data.dataset_of_movies:
        repo.add_movie(movie)


def load_review_and_user(repo: MemoryRepository):
    # load default review for default user into repository, then load default user into repository.
    review = Review(
        movie=repo.get_movie(1),
        txt='GOTG is my new favourite movie of all time!',
        rating=10
    )
    user = User(username='nton939', password=generate_password_hash('nton939Password'))
    user.add_review(review)
    repo.add_review(review)
    repo.add_user(user)


def load_watchlist(repo: MemoryRepository):
    # load default watchlist for default user.
    movies = repo.get_movies_by_rank([1, 2, 3, 4, 5])
    watchlist = WatchList(user=repo.get_user('nton939'), watchlist_name='Watch Later')
    for movie in movies:
        watchlist.add_movie(movie)
    repo.add_watchlist(watchlist)


def populate(data_path: str, repo: MemoryRepository):
    # Load directors, genres, actors and movies into the repository.
    load_data(data_path, repo)

    # Load default review and user into the repository.
    load_review_and_user(repo)

    # Load default watchlist into the repository.
    load_watchlist(repo)
