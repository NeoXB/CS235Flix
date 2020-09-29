from datetime import date
from movie_app.authentication.services import AuthenticationException
from movie_app.authentication import services as auth_services
from movie_app.movies import services as movies_services
from movie_app.movies.services import NonExistentMovieException
import pytest


def test_can_add_user(in_memory_repo):
    new_username = 'yeezy'
    new_password = 'Abcd1234'
    auth_services.add_user(new_username, new_password, in_memory_repo)
    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')    # Check password is encrypted.


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'nton939'
    password = 'Abcd1234'
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'new_user'
    new_password = 'Abcd1234'
    auth_services.add_user(new_username, new_password, in_memory_repo)
    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'new_user'
    new_password = 'Abcd1234'
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

"""CHECKPOINT"""
def test_cannot_get_article_with_non_existent_id(in_memory_repo):
    article_id = 7

    # Call the service layer to attempt to retrieve the Article.
    with pytest.raises(news_services.NonExistentArticleException):
        news_services.get_article(article_id, in_memory_repo)


def test_get_first_article(in_memory_repo):
    article_as_dict = news_services.get_first_article(in_memory_repo)

    assert article_as_dict['id'] == 1


def test_get_last_article(in_memory_repo):
    article_as_dict = news_services.get_last_article(in_memory_repo)

    assert article_as_dict['id'] == 6


def test_get_articles_by_date_with_one_date(in_memory_repo):
    target_date = date.fromisoformat('2020-02-28')

    articles_as_dict, prev_date, next_date = news_services.get_articles_by_date(target_date, in_memory_repo)

    assert len(articles_as_dict) == 1
    assert articles_as_dict[0]['id'] == 1

    assert prev_date is None
    assert next_date == date.fromisoformat('2020-02-29')


def test_get_articles_by_date_with_multiple_dates(in_memory_repo):
    target_date = date.fromisoformat('2020-03-01')

    articles_as_dict, prev_date, next_date = news_services.get_articles_by_date(target_date, in_memory_repo)

    # Check that there are 3 articles dated 2020-03-01.
    assert len(articles_as_dict) == 3

    # Check that the article ids for the the articles returned are 3, 4 and 5.
    article_ids = [article['id'] for article in articles_as_dict]
    assert set([3, 4, 5]).issubset(article_ids)

    # Check that the dates of articles surrounding the target_date are 2020-02-29 and 2020-03-05.
    assert prev_date == date.fromisoformat('2020-02-29')
    assert next_date == date.fromisoformat('2020-03-05')


def test_get_articles_by_date_with_non_existent_date(in_memory_repo):
    target_date = date.fromisoformat('2020-03-06')

    articles_as_dict, prev_date, next_date = news_services.get_articles_by_date(target_date, in_memory_repo)

    # Check that there are no articles dated 2020-03-06.
    assert len(articles_as_dict) == 0


def test_get_articles_by_id(in_memory_repo):
    target_article_ids = [5, 6, 7, 8]
    articles_as_dict = news_services.get_articles_by_id(target_article_ids, in_memory_repo)

    # Check that 2 articles were returned from the query.
    assert len(articles_as_dict) == 2

    # Check that the article ids returned were 5 and 6.
    article_ids = [article['id'] for article in articles_as_dict]
    assert set([5, 6]).issubset(article_ids)


def test_get_comments_for_article(in_memory_repo):
    comments_as_dict = news_services.get_comments_for_article(1, in_memory_repo)

    # Check that 2 comments were returned for article with id 1.
    assert len(comments_as_dict) == 2

    # Check that the comments relate to the article whose id is 1.
    article_ids = [comment['article_id'] for comment in comments_as_dict]
    article_ids = set(article_ids)
    assert 1 in article_ids and len(article_ids) == 1


def test_get_comments_for_non_existent_article(in_memory_repo):
    with pytest.raises(NonExistentArticleException):
        comments_as_dict = news_services.get_comments_for_article(7, in_memory_repo)


def test_get_comments_for_article_without_comments(in_memory_repo):
    comments_as_dict = news_services.get_comments_for_article(2, in_memory_repo)
    assert len(comments_as_dict) == 0

