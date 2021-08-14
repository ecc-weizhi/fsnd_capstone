import json
from json import JSONDecodeError

from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import SQLAlchemyError

from app.client_error_exception import BadRequest, UnprocessableEntity, NotFound
from auth.auth import requires_auth
from models import db
from models.actor import Actor

actors_blueprint = Blueprint("actors", __name__, url_prefix="/actors")
ACTOR_PAGE_SIZE = 10


@actors_blueprint.route("")
@requires_auth("get:actors")
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
@requires_auth("delete:actors")
def delete(actor_id):
    try:
        actor = Actor.query.filter_by(id=actor_id).first()
        if not actor:
            raise NotFound("Actor", actor_id)
        actor.delete()
        db.session.commit()
        is_success = True
    except SQLAlchemyError:
        is_success = False

    if is_success:
        return jsonify({
            "success": is_success,
            "deleted_id": actor_id
        })
    else:
        abort(500)


@actors_blueprint.route("", methods=["POST"])
@requires_auth("post:actors")
def post():
    data_string = request.data
    try:
        request_json = json.loads(data_string)
    except JSONDecodeError:
        raise BadRequest()

    # error checking
    field_name = request_json.get("name", None)
    field_age = request_json.get("age", None)
    field_gender = request_json.get("gender", None)

    missing_field = []
    if not field_name:
        missing_field.append("name")
    if not field_age:
        missing_field.append("age")
    if not field_gender:
        missing_field.append("gender")

    if missing_field:
        raise UnprocessableEntity(missing_field)

    actor = Actor(
        field_name,
        field_age,
        field_gender,
    )

    try:
        db.session.add(actor)
        db.session.commit()
        is_success = True
    except SQLAlchemyError:
        is_success = False

    if is_success:
        return jsonify({
            "success": is_success,
            "actor": actor.format(),
        })
    else:
        abort(500)


@actors_blueprint.route("/<int:actor_id>", methods=["PATCH"])
@requires_auth("patch:actors")
def patch(actor_id):
    actor = Actor.query.filter_by(id=actor_id).first()
    if not actor:
        raise NotFound("Actor", actor_id)

    data_string = request.data
    try:
        request_json = json.loads(data_string)
    except JSONDecodeError:
        raise BadRequest()

    # error checking
    field_name = request_json.get("name", None)
    field_age = request_json.get("age", None)
    field_gender = request_json.get("gender", None)

    missing_field = []
    if not field_name:
        missing_field.append("name")
    if not field_age:
        missing_field.append("age")
    if not field_gender:
        missing_field.append("gender")

    if missing_field:
        raise UnprocessableEntity(missing_field)

    actor.name = field_name
    actor.age = field_age
    actor.gender = field_gender

    try:
        db.session.commit()
        is_success = True
    except SQLAlchemyError:
        is_success = False

    if is_success:
        return jsonify({
            "success": is_success,
            "actor": actor.format(),
        })
    else:
        abort(500)
