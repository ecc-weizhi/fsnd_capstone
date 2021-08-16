import os

from flask_sqlalchemy import SQLAlchemy

local_database_path = "postgresql://weizhi:test1234@localhost:5432/castingcouch"

db = SQLAlchemy()


def setup_db(app, database_path=local_database_path):
    database_uri = os.environ.get("DATABASE_URL", None) \
        if os.environ.get("IS_HEROKU", None) else local_database_path
    if database_uri.startswith("postgres://"):
        database_uri = database_uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
