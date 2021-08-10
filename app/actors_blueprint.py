from flask import Blueprint

actors_blueprint = Blueprint("actors", __name__, url_prefix="/actors")


@actors_blueprint.route("")
def get():
    pass


@actors_blueprint.route("/<int:actor_id>", methods=["DELETE"])
def delete(actor_id):
    pass


@actors_blueprint.route("", methods=["POST"])
def post():
    pass


@actors_blueprint.route("/<int:actor_id>", methods=["PATCH"])
def patch(actor_id):
    pass
