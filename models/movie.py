from sql_alchemy import database

class MovieModel(database.Model):

    __tablename__ = 'movies'
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50))
    rating = database.Column(database.String(5))
    duration = database.Column(database.Integer)

    def __init__(self, id, name, rating, duration, created_at):
        self.id = id
        self.name = name
        self.rating = rating
        self.duration = duration
        self.created_at = created_at

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'rating': self.rating,
                'duration': self.duration,
                'created_at': self.created_at
                }
    @classmethod
    def find_movie_by_id(cls, id):
        movie = cls.query.filter_by(id=id).first()
        if movie:
            return movie
        return ""
    def save_movie(self):
        database.session.add(self)
        database.session.commit()
