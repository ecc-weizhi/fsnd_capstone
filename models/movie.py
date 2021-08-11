from models import db


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Movie id:{self.id}, " \
               f"title:{self.title}, " \
               f"release_date:{self.release_date}>"
