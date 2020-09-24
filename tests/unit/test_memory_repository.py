from datetime import date, datetime
from typing import List
from movie_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList
from movie_app.adapters.repository import RepositoryException
import pytest


def test_repo_can_add_director(in_memory_repo):
    director = Director('Peter Jackson')
    in_memory_repo.add_director(director)
    assert in_memory_repo.get_director('Peter Jackson') is director


def test_repo_can_retrieve_director(in_memory_repo):
    director = in_memory_repo.get_director('James Gunn')
    assert director == Director('James Gunn')


def test_repo_does_not_retrieve_non_existent_director(in_memory_repo):
    director = in_memory_repo.get_director('Bob')
    assert director is None


def test_repo_can_add_genre(in_memory_repo):
    genre = Genre('Anime')
    in_memory_repo.add_genre(genre)
    assert genre in in_memory_repo.get_genres()


def test_repo_can_retrieve_genres(in_memory_repo):
    genres: List[Genre] = in_memory_repo.get_genres()
    assert len(genres) == 10


def test_repo_can_add_actor(in_memory_repo):
    actor = Actor('Vin Diesel')
    in_memory_repo.add_actor(actor)
    assert in_memory_repo.get_actor('Vin Diesel') is actor


def test_repo_can_retrieve_actor(in_memory_repo):
    actor = in_memory_repo.get_actor('Vin Diesel')
    assert actor == Actor('Vin Diesel')


def test_repo_does_not_retrieve_non_existent_actor(in_memory_repo):
    actor = in_memory_repo.get_actor('Ace')
    assert actor is None


def test_repo_can_retrieve_movie_count(in_memory_repo):
    no_of_movies = in_memory_repo.get_number_of_movies()
    assert no_of_movies == 1000


def test_repo_can_add_movie(in_memory_repo):
    movie = Movie('New Movie', 2020)
    movie.rank = 1001
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie(1001) is movie


def test_repo_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    # Check that the Movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the Movie is reviewed as expected.
    user = in_memory_repo.get_user('nton939')
    assert user.reviews[0].review_text == 'GOTG is my new favourite movie of all time!'

    # Check that the Movie has the expected genres.
    assert movie.genres == [Genre('Action'), Genre('Adventure'), Genre('Sci-Fi')]


def test_repo_does_not_retrieve_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(0)
    assert movie is None

"""CHECKPOINT"""
def test_repository_can_retrieve_articles_by_date(in_memory_repo):
    articles = in_memory_repo.get_articles_by_date(date(2020, 3, 1))

    # Check that the query returned 3 Articles.
    assert len(articles) == 3


def test_repository_does_not_retrieve_an_article_when_there_are_no_articles_for_a_given_date(in_memory_repo):
    articles = in_memory_repo.get_articles_by_date(date(2020, 3, 8))
    assert len(articles) == 0


def test_repository_can_get_first_article(in_memory_repo):
    article = in_memory_repo.get_first_article()
    assert article.title == 'Coronavirus: First case of virus in New Zealand'


def test_repository_can_get_last_article(in_memory_repo):
    article = in_memory_repo.get_last_article()
    assert article.title == 'Coronavirus: Death confirmed as six more test positive in NSW'


def test_repository_can_get_articles_by_ids(in_memory_repo):
    articles = in_memory_repo.get_articles_by_id([2, 5, 6])

    assert len(articles) == 3
    assert articles[
               0].title == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'
    assert articles[1].title == "Australia's first coronavirus fatality as man dies in Perth"
    assert articles[2].title == 'Coronavirus: Death confirmed as six more test positive in NSW'


def test_repository_does_not_retrieve_article_for_non_existent_id(in_memory_repo):
    articles = in_memory_repo.get_articles_by_id([2, 9])

    assert len(articles) == 1
    assert articles[
               0].title == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    articles = in_memory_repo.get_articles_by_id([0, 9])

    assert len(articles) == 0


def test_repository_returns_article_ids_for_existing_tag(in_memory_repo):
    article_ids = in_memory_repo.get_article_ids_for_tag('New Zealand')

    assert article_ids == [1, 3, 4]


def test_repository_returns_an_empty_list_for_non_existent_tag(in_memory_repo):
    article_ids = in_memory_repo.get_article_ids_for_tag('United States')

    assert len(article_ids) == 0


def test_repository_returns_date_of_previous_article(in_memory_repo):
    article = in_memory_repo.get_article(6)
    previous_date = in_memory_repo.get_date_of_previous_article(article)

    assert previous_date.isoformat() == '2020-03-01'


def test_repository_returns_none_when_there_are_no_previous_articles(in_memory_repo):
    article = in_memory_repo.get_article(1)
    previous_date = in_memory_repo.get_date_of_previous_article(article)

    assert previous_date is None


def test_repository_returns_date_of_next_article(in_memory_repo):
    article = in_memory_repo.get_article(3)
    next_date = in_memory_repo.get_date_of_next_article(article)

    assert next_date.isoformat() == '2020-03-05'


def test_repository_returns_none_when_there_are_no_subsequent_articles(in_memory_repo):
    article = in_memory_repo.get_article(6)
    next_date = in_memory_repo.get_date_of_next_article(article)

    assert next_date is None


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    article = in_memory_repo.get_article(2)
    comment = make_comment("Trump's onto it!", user, article)

    in_memory_repo.add_comment(comment)

    assert comment in in_memory_repo.get_comments()


def test_repository_does_not_add_a_comment_without_a_user(in_memory_repo):
    article = in_memory_repo.get_article(2)
    comment = Comment(None, article, "Trump's onto it!", datetime.today())

    with pytest.raises(RepositoryException):
        in_memory_repo.add_comment(comment)


def test_repository_does_not_add_a_comment_without_an_article_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    article = in_memory_repo.get_article(2)
    comment = Comment(None, article, "Trump's onto it!", datetime.today())

    user.add_comment(comment)

    with pytest.raises(RepositoryException):
        # Exception expected because the Article doesn't refer to the Comment.
        in_memory_repo.add_comment(comment)


def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_comments()) == 2
