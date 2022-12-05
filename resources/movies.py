from flask_restful import Resource, reqparse
from models.movie import MovieModel
from pip._internal import req

users = [
    {'id': 1,
     'name': 'Grande Filme',
     'rating': 4.5,
     'duration': 120,
     'created_at': 2000},
    {'id': 2,
     'name': 'Grandíssimo Filme',
     'rating': 4.7,
     'duration': 123,
     'created_at': 2001},
    {'id': 3,
     'name': 'Grandíssissimo Filme',
     'rating': 5.0,
     'duration': 125,
     'created_at': 2002}
]

class Movies(Resource):
    def get(self):
        return users

class Movie(Resource):

    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('name')
    minha_requisicao.add_argument('rating')
    minha_requisicao.add_argument('duration')
    minha_requisicao.add_argument('created_at')

    def find_movie(id):
        for movie in users:
            if movie['id'] == id:
                return movie
        return None
    def find_last_movie(id):
        movie_id = 0
        for movie in users:
            if movie['id'] >= movie_id:
                movie_id = movie['id']
        return movie_id

    def get(self, id):
        #movie = MovieModel.find_movie_by_id(id)
        movie = Movie.find_movie(id)
        if movie:
            return [movie]#.json()
        return {'message': 'movie not found'}, 204

    def post(self, id):
        dados = Movie.minha_requisicao.parse_args()
        movie_id = Movie.find_last_movie(id) + 1

        new_movie = MovieModel(movie_id, **dados)
        users.append(new_movie)
        return new_movie, 200
    def put(self, id):
        dados = Movie.minha_requisicao.parse_args()
        movie = Movie.find_movie(id)
        if movie:
            new_movie = MovieModel(id, **dados)
            users.update(new_movie)
            return new_movie, 200
        else:
            movie_id = Movie.find_last_movie(id) + 1
            new_movie = MovieModel(movie_id, **dados)
            users.append(new_movie)
            return new_movie, 201

    def delete(self, id):
        global users
        movies = [movie for movie in movies if movie['id'] != id]
        return {'message' : 'movie deleted'}