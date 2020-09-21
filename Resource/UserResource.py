from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask_restplus import Namespace, Resource, reqparse
from Model.models import *
from Utils import AuthorizationDoc
from Utils.InputValidation import *
import html
import datetime
from geopy import distance

api = Namespace('user')


profile_req = reqparse.RequestParser()
profile_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)


class UserProfile(Resource):
    @jwt_required
    @api.expect(profile_req)
    @api.doc(security='Bearer Auth', authorizations=AuthorizationDoc.authorizations)
    def get(self):
        current_user = get_jwt_identity()
        user_details = UserDetails.find_by_id(current_user[1])
        return {'data': user_details.as_dict()}, 200


update_profile_req = reqparse.RequestParser()
update_profile_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)
update_profile_req.add_argument('first_name', type=str, default='')
update_profile_req.add_argument('last_name', type=str, default='')
update_profile_req.add_argument('new_password', type=str, default='')
update_profile_req.add_argument('old_password', type=str, default='')


class UserUpdateProfile(Resource):
    @jwt_required
    @api.expect(update_profile_req)
    @api.doc(security='Bearer Auth', authorizations=AuthorizationDoc.authorizations)
    def post(self):
        data = update_profile_req. parse_args()
        current_user = get_jwt_identity()

        user_details = UserDetails.find_by_id(current_user[1])
        if 0 < len(data['new_password']) < 5:
            return 'Password is too short', 400
        if not user_details.verify_hash(data['old_password'], user_details.password):
            return 'Wrong password', 400
        if len(data['first_name']) > 0:
            user_details.first_name = data['first_name']
        if len(data['last_name']) > 0:
            user_details.last_name = data['last_name']
        if len(data['new_password']) > 0:
            user_details.password = user_details.generate_hash(data['new_password'])
        user_details.save_to_db()
        return 'success', 200


rating_get_req = reqparse.RequestParser()
rating_get_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)
rating_get_req.add_argument('book_id', type=str, required=True)


rating_post_req = reqparse.RequestParser()
rating_post_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)
rating_post_req.add_argument('book_id', type=str, required=True)
rating_post_req.add_argument('rating_num', type=int, required=True)
rating_post_req.add_argument('rating_comment', type=str, default='')

class UserRate(Resource):
    @jwt_required
    @api.expect(rating_get_req)
    def get(self):
        data = rating_get_req.parse_args()
        current_user = get_jwt_identity()
        v = validate_book_id(data['book_id'])
        if not v[0]:
            return {'message': 'Book does not exsit!'}, 400
        book_details = v[1]
        rating_details = RatingDetails.find_existing(current_user[1], book_details.book_id)
        if not rating_details:
            return {
                'data': {
                    'rating_num': 0,
                    'rating_comment': ''
                 }
            }, 200
        return {'data': rating_details.as_dict()}, 200

    @jwt_required
    @api.expect(rating_post_req)
    @api.doc(security='Bearer Auth', authorizations=AuthorizationDoc.authorizations)
    def post(self):
        data = rating_post_req.parse_args()
        data['rating_comment'] = html.escape(data['rating_comment'])
        current_user = get_jwt_identity()
        # if not current_user:
        #     return {'message': 'You need login to rate this book', 'status': 'error'}, 401

        v = validate_book_id(data['book_id'])
        if not v[0]:
            return {'message': 'Book does not exsit!'}, 400

        if not 1 <= int(data['rating_num']) <= 5:
            return {'message': 'Rating num must be between 1 or 5'}, 400

        book_details = v[1]
        rating_details = RatingDetails.find_existing(current_user[1], book_details.book_id)
        if not rating_details:
            rating_details = RatingDetails(book_id=data['book_id'],
                                           user_id=current_user[1],
                                           rating_num=data['rating_num'],
                                           rating_comment=data['rating_comment'])
            book_details.add_rating(data['rating_num'])
        else:
            if rating_details.rating_num != data['rating_num']:
                book_details.swap_rating(rating_details.rating_num, data['rating_num'])
            rating_details.rating_num = data['rating_num']
            rating_details.rating_comment = data['rating_comment']
            rating_details.created_date = datetime.datetime.utcnow()
        rating_details.save_to_db()
        book_details.save_to_db()
        # update_ratings_book(book_details.book_id, book_details.get_average_rating())
        return {'message': 'success'}, 200


ratings_req = reqparse.RequestParser()
ratings_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)
ratings_req.add_argument('limit', type=int, default=5)
ratings_req.add_argument('page', type=int, default=1)

class UserRatings(Resource):
    @jwt_required
    @api.expect(ratings_req)
    @api.doc(security='Bearer Auth', authorizations=AuthorizationDoc.authorizations)
    def get(self):
        data = ratings_req.parse_args()
        current_user = get_jwt_identity()
        return RatingDetails.find_by_user(current_user[1], data['limit'], data['page'])


ratings_stat_req = reqparse.RequestParser()
ratings_stat_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)

class UserRatingsStat(Resource):
    @jwt_required
    @api.expect(ratings_stat_req)
    @api.doc(security='Bearer Auth', authorizations=AuthorizationDoc.authorizations)
    def get(self):
        data = ratings_req.parse_args()
        current_user = get_jwt_identity()
        return {'data': [
            {str(i): RatingDetails.find_by_user_and_rating_num(current_user[1], i)} for i in range(1, 6)
        ]}, 200


nearby_req = reqparse.RequestParser()
nearby_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)
nearby_req.add_argument('limit', type=int, default=5)
nearby_req.add_argument('page', type=int, default=1)
nearby_req.add_argument('radius', type=int, default=10)

class NearBy(Resource):
    @jwt_required
    @api.expect(nearby_req)
    @api.doc(security='Bearer Auth', authorizations=AuthorizationDoc.authorizations)
    def get(self):
        def func(x):
            okc_ok = (cur_user['latitude'], cur_user['longitude'])
            norman_ok = (x['latitude'], x['longitude'])
            return distance.distance(okc_ok, norman_ok).m
        try:
            data = nearby_req.parse_args()
            current_user = get_jwt_identity()
            all_user = UserDetails.return_all_pos()['users']
            other = []
            cur_user = None
            for user in all_user:
                if user['id'] == current_user[1]:
                    cur_user = user
                elif user['latitude'] is not None:
                    other.append(user)

            d = [] # distance
            users = []
            # Near by user
            for o_user in other:
                if func(o_user) <= data["radius"]:
                    d.append(func(o_user))
                    users.append(UserDetails.find_by_id(o_user['id']))
            # Get book_ids
            books = []
            for i in range(len(users)):
                for book in users[i].sharing_details:
                    books.append({'distance': d[i],'user' : users[i], 'book_id' : book.get_book_id()})
            books = books[(data.page - 1 ) * data.limit  : data.page * data.limit]

            result = {'data' : []}
            for book in books:
                book_detail = BookDetails.find_by_id(book['book_id'])
                result['data'].append({
                    'user' : book['user'].as_dict(),
                    'distance' : round(book['distance'],2 ),
                    'book_detail' : BookDetails.to_json(book_detail)
                })
            return result
        except:
            return {'message': 'Something went wrong'}, 200

updatepos_req = reqparse.RequestParser()
updatepos_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)
updatepos_req.add_argument('latitude', type=float)
updatepos_req.add_argument('longitude', type=float)

class UpdatePos(Resource):
    @jwt_required
    @api.expect(updatepos_req)
    @api.doc(security='Bearer Auth', authorizations=AuthorizationDoc.authorizations)
    def post(self):
        def func(x):
            okc_ok = (0, 0)
            norman_ok = (x['latitude'], x['longitude'])
            return distance.distance(okc_ok, norman_ok).m
        try:
            data = updatepos_req.parse_args()
            current_user = get_jwt_identity()
            func({"latitude" : data.latitude, "longitude" : data.longitude})
            user = UserDetails.find_by_id(current_user[1])
            result = user.update_position(data.latitude, data.longitude)
            if result:
                return {'message': 'success'}, 200
            else:
                return {'message': 'Something went wrong'}, 200
        except:
            return {'message': 'Something went wrong. Check your location value.'}, 200

sharing_req = reqparse.RequestParser()
sharing_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)
sharing_req.add_argument('book_id', type=str, required=True)

class UserShare(Resource):
    @jwt_required
    @api.expect(sharing_req)
    def post(self):
        data = sharing_req.parse_args()
        current_user = get_jwt_identity()
        v = validate_book_id(data['book_id'])
        if not v[0]:
            return {'message': 'Book does not exist!'}, 400
        sharing_details = SharingDetails.find_existing(current_user[1], data['book_id'])
        if not sharing_details:
            sharing_details = SharingDetails(user_id = current_user[1],book_id =  data['book_id'])
            sharing_details.save_to_db()
            return {'message': 'Success'}, 200
        return {'message' : 'Your book has been shared'}, 200

    @jwt_required
    @api.expect(sharing_req)
    def delete(self):
        data = sharing_req.parse_args()
        current_user = get_jwt_identity()
        v = validate_book_id(data['book_id'])
        if not v[0]:
            return {'message': 'Book does not exist!'}, 400
        sharing_details = SharingDetails.find_existing(current_user[1], data['book_id'])
        if sharing_details:
            SharingDetails.delete_record(current_user[1], data['book_id'])
            return {'message': 'Success'}, 200
        return {'message' : 'Some thing went wrong'}, 200


playlist_get_req = reqparse.RequestParser()
playlist_get_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)

playlist_post_req = reqparse.RequestParser()
playlist_post_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)
playlist_post_req.add_argument('playlist_name', type=str, required=True)

class UserPlaylist(Resource):
    @jwt_required
    @api.expect(playlist_get_req)
    def get(self):
        data = playlist_get_req.parse_args()
        current_user = get_jwt_identity()
        if not current_user:
            return {'message': 'You need login', 'status': 'error'}, 401

        result = {
            'data': list(map(lambda x: {
                'playlist_id': x.playlist_id,
                'name': x.name,
                'books_count': x.books_count
            },
                Playlist.return_by_user(current_user[1])))
        }
        return result

    @jwt_required
    @api.expect(playlist_post_req)
    @api.doc(security='Bearer Auth', authorizations=AuthorizationDoc.authorizations)
    def post(self):
        data = playlist_post_req.parse_args()
        current_user = get_jwt_identity()
        if not current_user:
            return {'message': 'You need login', 'status': 'error'}, 401

        if Playlist.find_existing(current_user[1], data['playlist_name']):
            return {'message': 'Playlist name exist!'}, 400

        playlist = Playlist(user_id=current_user[1], name=data['playlist_name'])
        playlist.save_to_db()

        return {'message' : 'success'}, 200


playlist_detail_get_req = reqparse.RequestParser()
playlist_detail_get_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)
playlist_detail_get_req.add_argument('playlist_id', type=int, required=True)
playlist_detail_get_req.add_argument('lang', type=str, choices=('vi', 'en'), default='vi')

playlist_detail_post_req = reqparse.RequestParser()
playlist_detail_post_req.add_argument('Authorization', type=str, location='headers', help='Bearer Access Token', required=True)
playlist_detail_post_req.add_argument('playlist_id', type=int, required=True)
playlist_detail_post_req.add_argument('book_id', type=int, required=True)

class PlaylistDetail(Resource):
    @jwt_required
    @api.expect(playlist_detail_get_req)
    def get(self):
        data = playlist_detail_get_req.parse_args()
        current_user = get_jwt_identity()
        if not current_user:
            return {'message': 'You need login', 'status': 'error'}, 401

        books_id = set()
        books_find_by_playlist = PlaylistDetails.find_by_playlist_id(data['playlist_id'])
        books_id.update(list(map(lambda x: x.book_id, books_find_by_playlist)))

        response = {}
        books = []
        for index, id in enumerate(books_id):
            v = BookDetails.get_book_details(id)
            book_details = v[1]
            books += list(map(lambda x: {
                'book_id': x.book_id,
                'book_title': x.book_title,
                'book_cover': x.book_cover,
                'rating': x.get_average_rating(),
                'author': x.author_details.author_name,
                'audio': extract_book_audio(x.book_audio)
            }, book_details))

            if data["lang"] == "vi":
                book_categories = BookCategories.find_by_book_id(id)
                books[index]["categories"] = [CategoryDetails.find_by_id(category.category_id).category_name_vi for
                                              category in book_categories]
            else:
                book_categories = BookCategories.find_by_book_id(id)
                books[index]["categories"] = [CategoryDetails.find_by_id(category.category_id).category_name_en for
                                              category in book_categories]
        response['data'] = books
        return response

    @jwt_required
    @api.expect(playlist_detail_post_req)
    @api.doc(security='Bearer Auth', authorizations=AuthorizationDoc.authorizations)
    def post(self):
        data = playlist_detail_post_req.parse_args()
        current_user = get_jwt_identity()
        if not current_user:
            return {'message': 'You need login', 'status': 'error'}, 401

        v = validate_book_id(data['book_id'])
        if not v[0]:
            return {'message': 'Book does not exist!'}, 400

        book_details = v[1]
        playlist_detail = PlaylistDetails.find_existing(data['playlist_id'], book_details.book_id)
        if not playlist_detail:
            playlist_detail = PlaylistDetails(playlist_id=data['playlist_id'],
                                                book_id=book_details.book_id)
            user_playlist = Playlist.return_by_playlist_id(data['playlist_id'])
            user_playlist.add_book()
            playlist_detail.save_to_db()
            return {'message': 'Success'}, 200
        else:
            return {'message': 'Book existed in playlist'}, 200

    @jwt_required
    @api.expect(playlist_detail_post_req)
    def delete(self):
        data = playlist_detail_post_req.parse_args()
        current_user = get_jwt_identity()
        v = validate_book_id(data['book_id'])
        if not v[0]:
            return {'message': 'Book does not exist!'}, 400
        book_details = v[1]
        playlist_detail = PlaylistDetails.find_existing(data['playlist_id'], book_details.book_id)
        if playlist_detail:
            PlaylistDetails.delete_record(data['playlist_id'], book_details.book_id)
            user_playlist = Playlist.return_by_playlist_id(data['playlist_id'])
            user_playlist.remove_book()
            return {'message': 'Success'}, 200
        else:
            return {'message': 'Book does not exist in playlist'}, 200


def extract_book_audio(audios):
    result = list(map(lambda x: x.url,audios))
    return result