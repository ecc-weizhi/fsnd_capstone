from flask import Blueprint

movies_blueprint = Blueprint("movies", __name__, url_prefix="/movies")


@movies_blueprint.route("")
def get():
    pass


@movies_blueprint.route("/<int:movie_id>", methods=['DELETE'])
def delete(movie_id):
    pass


@movies_blueprint.route("", methods=['POST'])
def post():
    pass


@movies_blueprint.route("/<int:movie_id>", methods=['PATCH'])
def patch(movie_id):
    pass
