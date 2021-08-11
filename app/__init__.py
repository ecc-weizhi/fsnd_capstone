from flask import Flask

from app.actors_blueprint import actors_blueprint
from app.movies_blueprint import movies_blueprint
from models import db

app = Flask(__name__)

app.register_blueprint(actors_blueprint)
app.register_blueprint(movies_blueprint)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://weizhi:test1234@localhost:5432/castingcouch"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)