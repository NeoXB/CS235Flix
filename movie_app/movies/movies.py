from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from movie_app.authentication.authentication import login_required
import movie_app.adapters.repository as repo
import movie_app.utilities.utilities as utilities
import movie_app.movies.services as services

# Configure Blueprint.
movies_blueprint = Blueprint('movies_bp', __name__)


@movies_blueprint.route('/movies_by_rank', methods=['GET'])
def movies_by_rank():
    movies_per_page = 3

    # Read query parameters.
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = 0
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    movie_ranks = list(range(1, 1001))

    # Retrieve the batch of movies to display on the web page.
    movies = services.get_movies_by_rank(movie_ranks[cursor:cursor + movies_per_page], repo.repo_instance)
    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_rank', cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_rank')

    if cursor + movies_per_page < len(movie_ranks):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_rank', cursor=cursor + movies_per_page)
        last_cursor = movies_per_page * int(len(movie_ranks) / movies_per_page)
        if len(movie_ranks) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_rank', cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews.
    for movie in movies:
        movie['view_review_url'] = url_for('movies_bp.movies_by_rank', cursor=cursor, view_reviews_for=movie['rank'])
        movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['rank'])
        movie['reviews'] = services.get_reviews_for_movie(movie['rank'], repo.repo_instance)

    # Generate the webpage to display the movies.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Ranked Movies',
        movies=movies,
        featured_movies=utilities.get_featured_movies(3),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews
    )


@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    movies_per_page = 3

    # Read query parameters.
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = 0
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)
    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ranks for movies that have genre genre_name.
    movie_ranks = services.get_movie_ranks_for_genre(genre_name, repo.repo_instance)

    # Retrieve the batch of movies to display on the web page.
    movies = services.get_movies_by_rank(movie_ranks[cursor:cursor + movies_per_page], repo.repo_instance)
    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name)

    if cursor + movies_per_page < len(movie_ranks):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor + movies_per_page)
        last_cursor = movies_per_page * int(len(movie_ranks) / movies_per_page)
        if len(movie_ranks) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews.
    for movie in movies:
        movie['view_review_url'] = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor,
                                           view_reviews_for=movie['rank'])
        movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['rank'])
        movie['reviews'] = services.get_reviews_for_movie(movie['rank'], repo.repo_instance)

    # Generate the webpage to display the movies.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Movies with genre ' + genre_name,
        movies=movies,
        featured_movies=utilities.get_featured_movies(3),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews
    )


@movies_blueprint.route('/movie_after_review', methods=['GET'])
def movie_after_review():
    # Read query parameters.
    movie_to_show_reviews = request.args.get('view_reviews_for')
    movie_rank = request.args.get('movie_rank')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = 0
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if movie_rank is None:
        # No movie_rank query parameter, so set to a non-existent movie rank.
        movie_rank = 0
    else:
        # Convert movie_rank from string to int.
        movie_rank = int(movie_rank)

    # Retrieve the movie to display on the web page.
    movie = services.get_movie(movie_rank, repo.repo_instance)

    # Construct urls for viewing movie reviews and adding reviews.
    movie['view_review_url'] = url_for('movies_bp.movie_after_review', view_reviews_for=movie['rank'],
                                       movie_rank=movie['rank'])
    movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['rank'])
    movie['reviews'] = services.get_reviews_for_movie(movie['rank'], repo.repo_instance)
    movies = [movie]
    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    # Generate the webpage to display the movie.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Thank you for reviewing!',
        movies=movies,
        featured_movies=utilities.get_featured_movies(3),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews
    )


@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with a movie rank, when subsequently called with a HTTP POST request, the movie rank remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the movie rank, representing the reviewed movie, from the form.
        movie_rank = int(form.movie_rank.data)

        # Use the service layer to store the new review.
        services.add_review(movie_rank, form.review.data, form.rating.data, username, repo.repo_instance)

        # Retrieve the movie in dict form.
        movie = services.get_movie(movie_rank, repo.repo_instance)

        return redirect(url_for('movies_bp.movie_after_review', view_reviews_for=movie_rank, movie_rank=movie_rank))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie rank, representing the movie to review, from a query parameter of the GET request.
        movie_rank = int(request.args.get('movie'))

        # Store the movie rank in the form.
        form.movie_rank.data = movie_rank
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the movie rank of the movie being reviewed from the form.
        movie_rank = int(form.movie_rank.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a web page that allows
    # the user to enter a review. The generated web page includes a form object.
    movie = services.get_movie(movie_rank, repo.repo_instance)
    return render_template(
        'movies/review_on_movie.html',
        title='Review Movie',
        movie=movie,
        form=form,
        handler_url=url_for('movies_bp.review_on_movie'),
        featured_movies=utilities.get_featured_movies(),
        genre_urls=utilities.get_genres_and_urls()
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Profanity is not allowed in reviews'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=2, message='Please write a longer review'),
        ProfanityFree(message='Profanity is not allowed in reviews')])
    rating = IntegerField('Rating', [
        DataRequired(),
        NumberRange(min=1, max=10, message='Please enter a number between 1 and 10')])
    movie_rank = HiddenField("Movie rank")
    submit = SubmitField('Submit')
