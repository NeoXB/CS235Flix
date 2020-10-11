import pytest
from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'anonymous', 'password': 'Iamanonymous1'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Please enter your username'),
        ('test', '', b'Please enter your password'),
        ('test', 'test', b'Password is invalid: it must have at least 7 characters, contain an upper case letter, \
            contain a lower case letter and contain a digit!'),
        ('nton939', 'Test#6^0', b'Username is already used - please try again'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'nton939'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_home(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'CS235Flix' in response.data


def test_login_required_to_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the review page.
    response = client.get('/review?movie=1')

    response = client.post(
        '/review',
        data={'review': 'wow!', 'rating': 10, 'movie_rank': 1}
    )
    assert response.headers['Location'] == 'http://localhost/movie_after_review?view_reviews_for=1&movie_rank=1'


@pytest.mark.parametrize(('review', 'rating', 'messages'), (
        ('Who thinks Trump is a fuckwit?', 1, (b'Profanity is not allowed in reviews')),
        ('a', 2, (b'Please write a longer review')),
))
def test_review_with_invalid_input(client, auth, review, rating, messages):
    # Login a user.
    auth.login()

    # Attempt to review a movie.
    response = client.post(
        '/comment',
        data={'review': review, 'rating': rating, 'movie_rank': 2}
    )
    # Check that supplying invalid review text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_movies_with_review(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_genre?genre=Action&cursor=0&view_reviews_for=1')
    assert response.status_code == 200

    # Check that all reviews for specified movie are included on the page.
    assert b'GOTG is my new favourite movie of all time!' in response.data


def test_movies_with_genre(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_genre?genre=Action')
    assert response.status_code == 200

    # Check that all movies with 'Sport' genre are included on the page.
    assert b'Movies with genre Action' in response.data
    assert b'Guardians of the Galaxy' in response.data
    assert b'Suicide Squad' in response.data
    assert b'The Great Wall' in response.data
