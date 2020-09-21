import sys

from flask_restplus import Namespace, Resource, reqparse
from Model.models import UserDetails
from Model.RevokedTokenModel import RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from Utils.InputValidation import *
import html
import json
import datetime


api = Namespace('auth')

parse = reqparse.RequestParser()
parse.add_argument('username', help="This field cannot be blank", required=True)
parse.add_argument('firstname', help="This field cannot be blank", required=True)
parse.add_argument('lastname', help="This field cannot be blank", required=True)
parse.add_argument('email', help="This field cannot be blank", required=True)
parse.add_argument('password', help="This field cannot be blank", required=True)


class UserRegistration(Resource):
    @api.expect(parse)
    def post(self):
        data = parse.parse_args()
        data['username'] = html.escape(data['username'])
        data['firstname'] = html.escape(data['firstname'])
        data['lastname'] = html.escape(data['lastname'])
        v = validate_new_email(data['email'])
        if not v[0]:
            return {'message': v[1]}, 400
        v = validate_new_user(data['username'])
        if not v[0]:
            return {'message': v[1]}, 400
        new_user = UserDetails(
            user_name=data['username'],
            first_name=data['firstname'],
            last_name=data['lastname'],
            email=data['email'],
            password=UserDetails.generate_hash(data['password'], )
        )
        try:
            new_user.save_to_db()
            playlist = Playlist(user_id=new_user.user_id, name='Yêu thích')
            playlist.save_to_db()
            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=(new_user.user_name, new_user.user_id), expires_delta=expires)
            refresh_token = create_refresh_token(identity=(new_user.user_name, new_user.user_id))
            return {
                'message': 'Success',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            e = sys.exc_info()[0]
            print(f'Error : {e}')
            return {'message': 'Something went wrong'}, 500


loginParse = reqparse.RequestParser()
loginParse.add_argument('username', help="This field cannot be blank", required=True)
loginParse.add_argument('password', help="This field cannot be blank", required=True)


class UserLogin(Resource):
    @api.expect(loginParse)
    def post(self):
        data = loginParse.parse_args()
        current_user = UserDetails.find_by_user_name(data['username'])
        if not current_user:
            return {'message': 'User name does not exist'}, 401

        if UserDetails.verify_hash(data['password'], current_user.password):
            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=(data['username'], current_user.user_id), expires_delta=expires)
            refresh_token = create_refresh_token(identity=(data['username'], current_user.user_id))
            return {
                'message': 'Success',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        expires = datetime.timedelta(days=365)
        access_token = create_access_token(identity=current_user, expires_delta=expires)
        return {'access_token': access_token}


class GetAllUsers(Resource):
    def get(self):
        return UserDetails.return_all()


class DelAllUsers(Resource):
    def delete(self):
        return UserDetails.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        try:
            current_user = get_jwt_identity()
            print(current_user)
        except:
            return {'message': 'Access token is revoked'}, 401
        return {
            'answer': 42
        }
