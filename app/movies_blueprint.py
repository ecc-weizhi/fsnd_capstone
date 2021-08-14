import json
from json import JSONDecodeError

from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import SQLAlchemyError

from app.client_error_exception import BadRequest, UnprocessableEntity, NotFound
from models import db
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
    try:
        movie = Movie.query.filter_by(id=movie_id).first()
        if not movie:
            raise NotFound("questions", movie_id)
        movie.delete()
        db.session.commit()
        is_success = True
    except SQLAlchemyError:
        is_success = False

    if is_success:
        return jsonify({
            "success": is_success,
            "deleted_id": movie_id
        })
    else:
        abort(500)


@movies_blueprint.route("", methods=['POST'])
def post():
    data_string = request.data
    try:
        request_json = json.loads(data_string)
    except JSONDecodeError:
        raise BadRequest()

    # error checking
    field_title = request_json.get("title", None)
    field_release_date = request_json.get("release_date", None)

    missing_field = []
    if not field_title:
        missing_field.append("title")
    if not field_release_date:
        missing_field.append("release_date")

    if missing_field:
        raise UnprocessableEntity(missing_field)

    movie = Movie(
        field_title,
        field_release_date,
    )

    try:
        db.session.add(movie)
        db.session.commit()
        is_success = True
    except SQLAlchemyError:
        is_success = False

    if is_success:
        return jsonify({
            "success": is_success,
            "movie": movie.format(),
        })
    else:
        abort(500)


@movies_blueprint.route("/<int:movie_id>", methods=['PATCH'])
def patch(movie_id):
    pass
