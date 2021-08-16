from flask_sqlalchemy import SQLAlchemy

database_path = "postgresql://weizhi:test1234@localhost:5432/castingcouch"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
