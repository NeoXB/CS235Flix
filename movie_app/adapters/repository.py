import abc
from typing import List
from movie_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_director(self, director: Director):
        """" Adds a Director to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_name) -> Director:
        """ Returns the Director named director_name from the repository.
        If there is no Director with the given director_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a Genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the Genres stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        """" Adds an Actor to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_name) -> Actor:
        """ Returns the Actor named actor_name from the repository.
        If there is no Actor with the given actor_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, rank: int) -> Movie:
        """ Returns Movie with rank from the repository.
        If there is no Movie with the given rank, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns the number of Movies in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns the first Movie, ordered by year, from the repository.
        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns the last Movie, ordered by year, from the repository.
        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_rank(self, rank_list):
        """ Returns a list of movies, whose ranks match those in rank_list, from the repository.
        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ranks_for_genre(self, genre_name: str):
        """ Returns a list of ranks representing Movies that are categorised by genre_name.
        If there are no Movies that are categorised by genre_name,
        this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.
        If the Review doesn't have links with a Movie,
        this method raises a RepositoryException and doesn't update the repository.
        """
        if review.movie is None:
            raise RepositoryException('Review not correctly attached to a Movie')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str) -> User:
        """ Returns the User named username from the repository.
        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_watchlist(self, watchlist: WatchList):
        """ Adds a WatchList to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_watchlist(self, user: User) -> List[WatchList]:
        """ Returns the WatchList owned by User from the repository.
        If the User does not own any watchlist, this method returns an empty list.
        """
        raise NotImplementedError
