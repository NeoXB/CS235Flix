from movie_app.domain.model \
    import Director, Genre, Actor, Movie, Review, User, WatchList, MovieWatchingSimulation

import pytest


# Director Unit Tests
def test_director_full_name():
    director1 = Director("Taika Waititi")
    assert repr(director1) == "<Director Taika Waititi>"
    director2 = Director("")
    assert director2.director_full_name is None
    director3 = Director(42)
    assert director3.director_full_name is None
    director4 = Director("")
    assert repr(director4) == "<Director None>"


def test_director_equal():
    director1 = Director("b")
    director2 = Director("B")
    assert (director1 != director2)


def test_director_lt():
    director1 = Director("Cameron Diaz")
    director2 = Director("Brad Pitt")
    assert (director1 > director2)


def test_director_hash():
    director1 = Director("Taika Waititi")
    assert hash(director1)


# Genre Unit Tests
def test_genre_name():
    genre1 = Genre("Comedy")
    assert repr(genre1) == "<Genre Comedy>"
    genre2 = Genre("")
    assert repr(genre2) == "<Genre None>"
    genre3 = Genre(0)
    assert genre3.genre_name is None


# Actor Unit Tests
def test_actor_full_name():
    a1 = Actor("Taika Waititi")
    assert repr(a1) == "<Actor Taika Waititi>"
    a2 = Actor("")
    assert a2.actor_full_name is None
    a3 = Actor(42)
    assert a3.actor_full_name is None
    a4 = Actor("")
    assert repr(a4) == "<Actor None>"


def test_actor_add_colleague():
    a1 = Actor("Taika Waititi")
    a2 = Actor("Bob bob")
    a1.add_actor_colleague(a2)
    assert a1.actor_colleague == [a2]
    a3 = Actor("")
    a1.add_actor_colleague(a3)
    assert a1.actor_colleague == [a2, a3]


def test_actor_check_colleague():
    a1 = Actor("Taika Waititi")
    a2 = Actor("Bob bob")
    a1.add_actor_colleague(a2)
    assert (a1.check_if_this_actor_worked_with(a2))


# Movie Unit Tests
def test_movie_lt():
    m1 = Movie("", 0)
    m2 = Movie("x", 0)
    assert (m1 < m2)


def test_movie_eq():
    m1 = Movie("wow", 0)
    m2 = Movie("wow", 1899)
    assert (m1 == m2)


def test_set_title():
    m1 = Movie("wow", 0)
    m1.title = "WOW"
    assert (m1.title == "WOW")


def test_add_actors():
    m1 = Movie("wow", 0)
    m1.actors = [Actor("a"), Actor("b"), Actor("c")]
    assert (m1.actors == [Actor("a"), Actor("b"), Actor("c")])


def test_one_director():
    m1 = Movie("wow", 0)
    with pytest.raises(Exception):
        m1.director = [Director("a"), Director("b")]


def test_description():
    m1 = Movie("wow", 0)
    m1.description = ""
    assert (m1.description == "")


def test_hash():
    m1 = Movie("wow", 2000)
    hash1 = hash("wow" + str(2000))
    assert(hash(m1) == hash1)


def test_repr():
    m1 = Movie("wow", 0)
    assert(repr(m1) == "<Movie wow, None>")


# Review Unit Tests
def test_review_eq():
    r1 = Review("", "", 0)
    r2 = Review("", "", 0)
    assert (r1 == r2)


# User Unit Tests
def test_username():
    user1 = User('Martin', 'pw12345')
    user2 = User('IAN', 'pw67890')
    user3 = User('daniel', 'pw87465')
    user4 = User('', '')
    assert (repr(user1) == "<User martin>")
    assert (repr(user2) == "<User ian>")
    assert (repr(user3) == "<User daniel>")
    assert (repr(user4) == "<User None>")


def test_user_eq():
    user1 = User('a', 'pw12345')
    user2 = User('b', 'pw67890')
    assert (user1 != user2)


def test_user_lt():
    user1 = User('a', 'pw12345')
    user2 = User('b', 'pw67890')
    assert (user2 > user1)


def test_user_hash():
    user1 = User('a', 'pw12345')
    user2 = User('a', 'pw67890')
    assert (hash(user1) == hash(user2))


def test_watch_movie():
    user1 = User('Martin', 'pw12345')
    m1 = Movie("a", 2000)
    m2 = Movie("b", 2000)
    m1.runtime_minutes = 10
    m2.runtime_minutes = 20
    user1.watch_movie(m1)
    user1.watch_movie(m2)
    assert (user1.time_spent_watching_movies_minutes == 30)
    assert (user1.watched_movies == [m1, m2])


def test_add_review():
    user1 = User('Martin', 'pw12345')
    m1 = Movie('a', 2000)
    r1 = Review(m1, 'wow', 10)
    user1.add_review(r1)
    assert (user1.reviews == [r1])


# WatchList Unit Tests
@pytest.fixture()
def w():
    return WatchList(User('ABC', '123'), "")


def test_default_name(w):
    assert w.watchlist_name == "New Watchlist"


def test_iter_and_next(w):
    w.add_movie(Movie("Moana", 2016))
    w.add_movie(Movie("Ice Age", 2002))
    w.add_movie(Movie("Guardians of the Galaxy", 2012))
    iterable = iter(w)
    assert next(iterable) == Movie("Moana", 2016)


def test_add_and_remove_movie(w):
    w.add_movie(Movie("Moana", 2016))
    w.remove_movie(Movie("Moana", 2016))
    assert w.watchlist == []


def test_select_movie(w):
    w.add_movie(Movie("Moana", 2016))
    assert w.select_movie_to_watch(0) == Movie("Moana", 2016)


def test_size(w):
    w.add_movie(Movie("Moana", 2016))
    assert w.size() == 1


def test_first_movie_in_watchlist(w):
    w.add_movie(Movie("Moana", 2016))
    w.add_movie(Movie("Ice Age", 2002))
    w.add_movie(Movie("Guardians of the Galaxy", 2012))
    assert w.first_movie_in_watchlist() == Movie("Moana", 2016)


def test_clear_watchlist(w):
    w.add_movie(Movie("Moana", 2016))
    w.add_movie(Movie("Ice Age", 2002))
    w.add_movie(Movie("Guardians of the Galaxy", 2012))
    w.clear_watchlist()
    assert w.watchlist == []


def test_share_watchlist(w):
    w.add_movie(Movie("Moana", 2016))
    w.add_movie(Movie("Ice Age", 2002))
    w.add_movie(Movie("Guardians of the Galaxy", 2012))
    user1 = User("DEF", "wow")
    w1 = w.share_watchlist(user1)
    assert w1.watchlist_owner == user1
    assert w1.watchlist == w.watchlist


def test_sort_by_title(w):
    m1 = Movie("Moana", 2016)
    m2 = Movie("Ice Age", 2002)
    m3 = Movie("Guardians of the Galaxy", 2012)
    w.add_movie(m1)
    w.add_movie(m2)
    w.add_movie(m3)
    watchlist = w.sort_watchlist_by_title()
    assert watchlist == [m3, m2, m1]


def test_sort_by_year(w):
    m1 = Movie("Moana", 2016)
    m2 = Movie("Ice Age", 2002)
    m3 = Movie("Guardians of the Galaxy", 2012)
    w.add_movie(m1)
    w.add_movie(m2)
    w.add_movie(m3)
    watchlist = w.sort_watchlist_by_year()
    assert watchlist == [m2, m3, m1]


def test_sort_by_runtime(w):
    m1 = Movie("Moana", 2016)
    m2 = Movie("Ice Age", 2002)
    m3 = Movie("Guardians of the Galaxy", 2012)
    m1.runtime_minutes = 1
    m2.runtime_minutes = 100
    m3.runtime_minutes = 10
    w.add_movie(m1)
    w.add_movie(m2)
    w.add_movie(m3)
    watchlist = w.sort_watchlist_by_runtime()
    assert watchlist == [m1, m3, m2]


def test_change_watchlist_name(w):
    w.change_watchlist_name("WOW")
    assert w.watchlist_name == "WOW"


# MovieWatchingSimulation Unit Tests
@pytest.fixture()
def simulation():
    return MovieWatchingSimulation(User('ABC', '123'), Movie("WOW", 2020))


def test_add_user(simulation):
    simulation.add_user(User('X', '123456'))
    simulation.add_user(User('Y', '00000'))
    simulation.add_user(User('Z', 'abcd'))
    assert simulation.watch_group == [User('ABC', '123'), User('X', '123456'), User('Y', '00000'), User('Z', 'abcd')]


def test_remove_user(simulation):
    simulation.add_user(User('X', '123456'))
    simulation.add_user(User('Y', '00000'))
    simulation.add_user(User('Z', 'abcd'))
    simulation.remove_user(User('X', '123456'))
    simulation.remove_user(User('Y', '00000'))
    simulation.remove_user(User('Z', 'abcd'))
    simulation.remove_user(User('ABC', '123'))
    assert simulation.watch_group == [simulation.administrator]


def test_change_movie(simulation):
    simulation.change_movie(Movie("NEW", 2021))
    assert simulation.movie_to_watch == Movie("NEW", 2021)


def test_write_review_for_everyone(simulation):
    u1 = User('X', '123456')
    simulation.add_user(u1)
    r1 = Review(Movie('WOW', 2020), "A very good movie", 10)
    simulation.write_review_for_everyone(r1)
    assert len(simulation.administrator.reviews) == 1
    assert u1.reviews[0].movie == Movie('WOW', 2020)


def test_update_user_information(simulation):
    u1 = User('X', '123456')
    u2 = User('Y', '00000')
    simulation.add_user(u1)
    simulation.add_user(u2)
    m1 = Movie("NEW", 2021)
    m1.runtime_minutes = 100
    simulation.change_movie(m1)
    simulation.update_user_information()
    assert len(simulation.administrator.watched_movies) == 1
    assert u1.watched_movies[0] == m1
    assert u2.time_spent_watching_movies_minutes == 100
