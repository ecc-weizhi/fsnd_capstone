import os

from flask import Flask, send_from_directory

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
        host = "https://fsnd-capstone-weizhi.herokuapp.com" \
            if os.environ.get("IS_HEROKU", None) else "http://127.0.0.1:5000"

        auth0_login_url = f"https://eccweizhi-fsnd.us.auth0.com/authorize?audience=myFoobar&response_type=token&client_id=5IBYZMcKkw8WfZOBHxtfpvczvBK7Szms&redirect_uri={host}/login-result"
        return f'<html><body><a href="{auth0_login_url}">Login auth0</a></body></html>'

    @app.route("/login-result")
    def login_result():
        return send_from_directory("../static", "login_result.html")

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
