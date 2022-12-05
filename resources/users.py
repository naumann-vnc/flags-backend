from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token

minha_requisicao = reqparse.RequestParser()
minha_requisicao.add_argument('login', type=str, required=True, help="login is required")
minha_requisicao.add_argument('password', type=str, required=True, help="password is required")


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if user:
            return user.json(), 200
        return {'message': 'user not found'}, 200  # or 204

    def delete(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if user:
            user.delete_user()
            return {'message': 'user deleted.'}, 200
        return {'message': 'user not found'}, 204

    def post(self, user_id):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        dados = minha_requisicao.parse_args()
        if UserModel.find_user_by_login(dados['login']):
            return {'message': 'Login {} already exists'.format(dados['login'])}, 200

        user_id = UserModel.find_last_user()
        dados = minha_requisicao.parse_args()
        new_user = UserModel(user_id, **dados)

        try:
            print(new_user.json())
            new_user.save_user()
        except:
            return {'message': 'An internal error ocurred.'}, 500

        return new_user.json(), 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = minha_requisicao.parse_args()
        user = UserModel.find_user_by_login(dados['login'])

        if user and user.password == dados['password']:
            token_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_acesso}, 200
        return {'message': 'User or password is not correct.'}, 200
