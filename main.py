from flask import Flask, request, jsonify, Response
from flask_restful import Api, Resource, reqparse
from resources.movies import Movies, Movie
from resources.users import User, UserLogin
from flask_jwt_extended import JWTManager, jwt_required
from flask_cors import CORS, cross_origin
from models.user import UserModel

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
jwt = JWTManager(app)

# conexão com mysql
#DATABASE_URI = 'mysql+pymysql://root@localhost/aula?charset=utf8mb4'
#app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['CORS_HEADERS'] = 'Content-Type'

#conexão com postgres
DATABASE_URI = 'postgresql+psycopg2://postgres:admin@localhost:5432/dbpython'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'Senai2022'
#@app.before_first_request
#@app
@cross_origin()
def create_database():
    database.create_all()

api.add_resource(Movies, '/movies')
api.add_resource(Movie, '/movies/<int:id>')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserLogin, '/login')

minha_requisicao = reqparse.RequestParser()
minha_requisicao.add_argument('user_id', type=str, required=True, help="password is required")
minha_requisicao.add_argument('email', type=str, required=True, help="email is required")
minha_requisicao.add_argument('password', type=str, required=True, help="password is required")

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def controller():
    if request.method == 'POST':
        return post()
    elif request.method == 'GET':
        return get()
    elif request.method == 'DELETE':
        return delete()
    else:
        return "Method not allowed"
def post():
    dados = minha_requisicao.parse_args()
    if UserModel.find_user_by_login(dados['email']):
        return {'message': 'Login {} already exists'.format(dados['email'])}, 203
    user_id = int(UserModel.find_last_user())
    print(user_id)
    dados = minha_requisicao.parse_args()
    new_user = UserModel(user_id, dados['email'], dados['password'])
    try:
        print(new_user.json())
        new_user.save_user()
    except:
        return {'message': 'An internal error ocurred.'}, 500
    return new_user.json(), 201
@jwt_required()
def get():
    dados = minha_requisicao.parse_args()
    user = UserModel.find_user_by_id(int(dados['user_id']))
    if user:
        return user.json(), 200
    return {'message': 'user not found'}, 200  # or 204
#@jwt_required
def delete():
    user = UserModel.find_user_by_id(int(dados['user_id']))
    if user:
        user.delete_user()
        return {'message': 'user deleted.'}, 200
    return {'message': 'user not found'}, 204
@app.route('/login', methods=['POST'])
def post():
        dados = minha_requisicao.parse_args()
        user = UserModel.find_user_by_login(dados['login'])

        if user and user.password == dados['password']:
            token_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_acesso}, 200
        return {'message': 'User or password is not correct.'}, 401

@app.route('/auth', methods=['POST'])
@jwt_required()
def auth_post():
        return {'auth': 'ok'}, 200

if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(host="172.31.60.5", port="8080", debug=True)
