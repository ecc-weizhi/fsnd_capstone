from flask import Blueprint, request, jsonify

from models.movie import Movie

movies_blueprint = Blueprint("movies", __name__, url_prefix="/movies")
MOVIE_PAGE_SIZE = 10


@movies_blueprint.route("")
def get():
    page = request.args.get('page', 1, type=int)

    start_index_inclusive = (page - 1) * MOVIE_PAGE_SIZE
    end_index_exclusive = start_index_inclusive + MOVIE_PAGE_SIZE

    movies = Movie.query.all()
    formatted_movies = [movie.format() for movie in movies]

    return jsonify({
        "success": True,
        "actors": formatted_movies[start_index_inclusive:end_index_exclusive],
    })


@movies_blueprint.route("/<int:movie_id>", methods=['DELETE'])
def delete(movie_id):
    pass


@movies_blueprint.route("", methods=['POST'])
def post():
    pass


@movies_blueprint.route("/<int:movie_id>", methods=['PATCH'])
def patch(movie_id):
    pass
