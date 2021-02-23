from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import current_app

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = current_app.config.get('API_USERNAME') or 'admin'
        passwd = current_app.config.get('API_PASSWORD') or 'admin'

        if safe_str_cmp(user, data['username']) and safe_str_cmp(passwd, data['password']):
            access_token = create_access_token(identity=user, fresh=True)
            refresh_token = create_refresh_token(user)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {"message": "Invalid Credentials!"}, 401
