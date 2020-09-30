from movie_app.authentication import services as auth_services
from movie_app.authentication.services import AuthenticationException
from movie_app.movies import services as movies_services
from movie_app.movies.services import NonExistentMovieException
from movie_app.utilities import services as utility_services
import pytest


def test_can_add_user(in_memory_repo):
    new_username = 'yeezy'
    new_password = 'Abcd123'
    auth_services.add_user(new_username, new_password, in_memory_repo)
    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')    # Check password is encrypted.


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'nton939'
    password = 'Abcd123'
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'new_user'
    new_password = 'Abcd123'
    auth_services.add_user(new_username, new_password, in_memory_repo)
    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'new_user'
    new_password = 'Abcd123'
    auth_services.add_user(new_username, new_password, in_memory_repo)
    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '123456789', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_rank = 1000
    review_text = 'Maybe there were ten lives?'
    rating = 8
    username = 'nton939'

    # Call the service layer to add the review.
    movies_services.add_review(movie_rank, review_text, rating, username, in_memory_repo)

    # Retrieve the reviews for the movie from the repo.
    reviews_as_dict = movies_services.get_reviews_for_movie(movie_rank, in_memory_repo)

    # Check that the reviews include a review with the new review text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict
         if dictionary['review_text'] == review_text), None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_rank = 0
    review_text = "I do not like this movie..."
    rating = 1
    username = 'nton939'

    # Call the service layer to attempt to add the review.
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.add_review(movie_rank, review_text, rating, username, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_rank = 1
    review_text = 'That was such a cool movie!'
    rating = 9
    username = 'bob'

    # Call the service layer to attempt to add the review.
    with pytest.raises(movies_services.UnknownUserException):
        movies_services.add_review(movie_rank, review_text, rating, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_rank = 1
    movie_as_dict = movies_services.get_movie(movie_rank, in_memory_repo)
    assert movie_as_dict['rank'] == movie_rank
    assert movie_as_dict['title'] == 'Guardians of the Galaxy'
    assert movie_as_dict['release_year'] == 2014
    assert movie_as_dict['description'] == 'A group of intergalactic criminals are forced to work together to stop ' \
                                           'a fanatical warrior from taking control of the universe.'
    assert movie_as_dict['runtime_minutes'] == 121
    assert movie_as_dict['rating'] == 8.1
    assert movie_as_dict['votes'] == 757074
    assert movie_as_dict['revenue'] == 333.13
    assert movie_as_dict['metascore'] == 76
    director_as_dict = movie_as_dict['director']
    assert 'James Gunn' == director_as_dict['director_name']
    assert len(movie_as_dict['actors']) == 4
    actor_names = [dictionary['actor_name'] for dictionary in movie_as_dict['actors']]
    assert 'Chris Pratt' in actor_names
    assert 'Vin Diesel' in actor_names
    assert 'Bradley Cooper' in actor_names
    assert 'Zoe Saldana' in actor_names
    assert len(movie_as_dict['genres']) == 3
    genre_names = [dictionary['genre_name'] for dictionary in movie_as_dict['genres']]
    assert 'Action' in genre_names
    assert 'Adventure' in genre_names
    assert 'Sci-Fi' in genre_names


def test_cannot_get_movie_with_non_existent_rank(in_memory_repo):
    movie_rank = 1500

    # Call the service layer to attempt to retrieve the movie.
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movie(movie_rank, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movies_services.get_first_movie(in_memory_repo)
    assert movie_as_dict['rank'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movies_services.get_last_movie(in_memory_repo)
    assert movie_as_dict['rank'] == 1000


def test_get_movies_by_rank(in_memory_repo):
    target_movie_ranks = [1, 2, 3]
    movies_as_dict = movies_services.get_movies_by_rank(target_movie_ranks, in_memory_repo)
    assert len(movies_as_dict) == 3
    movie_ranks = [movie['rank'] for movie in movies_as_dict]
    assert movie_ranks == target_movie_ranks


def test_get_reviews_for_movie(in_memory_repo):
    reviews_as_dict = movies_services.get_reviews_for_movie(1, in_memory_repo)
    assert len(reviews_as_dict) == 1
    movie_ranks = [review['movie_rank'] for review in reviews_as_dict]
    assert 1 in movie_ranks and len(movie_ranks) == 1


def test_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        reviews_as_dict = movies_services.get_reviews_for_movie(0, in_memory_repo)
        assert len(reviews_as_dict) == 0


def test_get_reviews_for_movie_without_reviews(in_memory_repo):
    reviews_as_dict = movies_services.get_reviews_for_movie(2, in_memory_repo)
    assert len(reviews_as_dict) == 0


def test_get_genres_from_utilities(in_memory_repo):
    genre_names = utility_services.get_genre_names(in_memory_repo)
    assert len(genre_names) == 20
    assert 'Action' in genre_names
