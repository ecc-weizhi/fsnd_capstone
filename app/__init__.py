from flask import Flask

from app.actors_blueprint import actors_blueprint
from app.client_error_exception import ClientErrorException
from app.error_handler import ErrorHandler
from app.movies_blueprint import movies_blueprint
from models import db

app = Flask(__name__)

app.register_blueprint(actors_blueprint)
app.register_blueprint(movies_blueprint)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://weizhi:test1234@localhost:5432/castingcouch"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

error_handler = ErrorHandler()


@app.errorhandler(ClientErrorException)
def client_error(error):
    return error_handler.handle_client_error(error)


@app.errorhandler(500)
def internal_server_error(error):
    return error_handler.handle_internal_server_error(error)
