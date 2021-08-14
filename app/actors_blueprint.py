from flask import Blueprint, request, jsonify

from models.actor import Actor

actors_blueprint = Blueprint("actors", __name__, url_prefix="/actors")
ACTOR_PAGE_SIZE = 10


@actors_blueprint.route("")
def get():
    page = request.args.get('page', 1, type=int)

    start_index_inclusive = (page - 1) * ACTOR_PAGE_SIZE
    end_index_exclusive = start_index_inclusive + ACTOR_PAGE_SIZE

    actors = Actor.query.all()
    formatted_actors = [actor.format() for actor in actors]

    return jsonify({
        "success": True,
        "actors": formatted_actors[start_index_inclusive:end_index_exclusive],
    })


@actors_blueprint.route("/<int:actor_id>", methods=["DELETE"])
def delete(actor_id):
    pass


@actors_blueprint.route("", methods=["POST"])
def post():
    pass


@actors_blueprint.route("/<int:actor_id>", methods=["PATCH"])
def patch(actor_id):
    pass
