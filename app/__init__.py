from flask import Flask

from app.actors_blueprint import actors_blueprint
from app.client_error_exception import ClientErrorException
from app.error_handler import ErrorHandler
from app.movies_blueprint import movies_blueprint
from auth.auth import AuthError
from models import setup_db


def create_app(test_config=None):
    app = Flask(__name__)

    app.register_blueprint(actors_blueprint)
    app.register_blueprint(movies_blueprint)

    setup_db(app)
    err_handler = ErrorHandler()

    @app.route("/")
    def root():
        return "Hello world"

    @app.errorhandler(ClientErrorException)
    def client_error(error):
        return err_handler.handle_client_error(error)

    @app.errorhandler(500)
    def internal_server_error(error):
        return err_handler.handle_internal_server_error(error)

    @app.errorhandler(AuthError)
    def auth_error(error):
        return err_handler.handle_auth_error(error)

    return app
