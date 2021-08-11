from models import db


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Actor id:{self.id}, " \
               f"name:{self.name}, " \
               f"age:{self.age}, " \
               f"gender:{self.gender}>"