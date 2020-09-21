# coding: utf-8

from flask import Flask, jsonify, request, render_template
from flask_restplus import Api
from flask_cors import CORS
from DB_Connection.db import init, sql_db
from flask_jwt_extended import JWTManager
from Model.RevokedTokenModel import RevokedTokenModel
import json
from Resource import UserValidationResource, UserResource, BookResource, CategoryResource, SearchResource\
    , RatingResource, BannerResource
import os
from Model.models import UserDetails
from Import_Data.import_data import ImportData



def factory():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    CORS(app)
    return app


app = factory()

with open('./Config/config.json') as json_data_file:
    data = json.load(json_data_file)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + data["user"] + ':' + data["password"] + '@' + data["host"] + ':' + str(data["port"]) + '/' + \
                                        data["database"] + "?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


init(app)
jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401

api = Api(app, version='1.0', title='mindBook API',
          description='mindBook API')

jwt._set_error_handler_callbacks(api)

auth_ns = api.namespace('auth', description='Authentication API')
user_ns = api.namespace('user', description='User API')
books_ns = api.namespace('books', description='Books API')
categories_ns = api.namespace('categories', description='Categories API')
search_ns = api.namespace('search', description='Search API')
rating_ns = api.namespace('ratings', description='Rating API')
banner_ns = api.namespace('banner', description='Banner API')
# Init db connection, create tables.

db = sql_db()
@app.before_first_request
def create_tables():
    db.create_all()
    # import_data = ImportData("/code")
    import_data = ImportData("E://Ky_II_2019_2020/PTUDDD/Mobile")
    import_data.import_authors()
    import_data.import_categories()
    import_data.import_books()
    import_data.import_audio()
    import_data.import_book_categories()


# ---------------------------AUTH----------------------------
auth_ns.add_resource(UserValidationResource.UserRegistration, '/registration')
auth_ns.add_resource(UserValidationResource.UserLogin, '/login')
auth_ns.add_resource(UserValidationResource.UserLogoutAccess, '/logout/access')
auth_ns.add_resource(UserValidationResource.UserLogoutRefresh, '/logout/refresh')
auth_ns.add_resource(UserValidationResource.TokenRefresh, '/token/refresh')
auth_ns.add_resource(UserValidationResource.SecretResource, '/secret')


# ---------------------------USER---------------------------
user_ns.add_resource(UserResource.UserProfile, '/profile')
user_ns.add_resource(UserResource.UserUpdateProfile, '/profile/update')
user_ns.add_resource(UserResource.UserRate, '/rate')
user_ns.add_resource(UserResource.NearBy, '/nearby')
user_ns.add_resource(UserResource.UpdatePos, '/position/update')
user_ns.add_resource(UserResource.UserShare, '/share')
user_ns.add_resource(UserResource.UserPlaylist, '/playlist')
user_ns.add_resource(UserResource.PlaylistDetail, '/playlist/detail')
# user_ns.add_resource(UserResource.UserRatings, '/ratings')


# ---------------------------BOOKS---------------------------
# books_ns.add_resource(BookResource.NewBook, '/new')
books_ns.add_resource(BookResource.AllBooksByCategory, '/category')
books_ns.add_resource(BookResource.DetailsBook, '/details')
books_ns.add_resource(BookResource.RatingsBook, '/ratings')
books_ns.add_resource(BookResource.TopBooks, '/trending')

# ---------------------------CATEGORIES---------------------------
categories_ns.add_resource(CategoryResource.AllCategory, '/')
categories_ns.add_resource(CategoryResource.PopularCategories, '/popular')

# --------------------------SEARCH------------------------------------
search_ns.add_resource(SearchResource.Search, '/')


# --------------------------RATING------------------------------------
rating_ns.add_resource(RatingResource.New, '/new')

# --------------------------RATING------------------------------------
banner_ns.add_resource(BannerResource.All, '/all')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)