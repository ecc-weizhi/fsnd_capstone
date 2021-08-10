from flask import Flask

from app.actors_blueprint import actors_blueprint
from app.movies_blueprint import movies_blueprint

app = Flask(__name__)

app.register_blueprint(actors_blueprint)
app.register_blueprint(movies_blueprint)