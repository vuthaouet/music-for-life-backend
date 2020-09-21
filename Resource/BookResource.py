from flask_restplus import Namespace, Resource, reqparse
from Model.models import BookDetails, UserDetails
from flask_jwt_extended import jwt_required
import html
from Utils.InputValidation import *

api = Namespace('books')

category_books_parse = reqparse.RequestParser()
category_books_parse.add_argument('category_id', type=int, required=True)
category_books_parse.add_argument('limit', type=int, default=10)
category_books_parse.add_argument('page', type=int, default=1)

class AllBooksByCategory(Resource):
    @api.expect(category_books_parse)
    def get(self):
        data = category_books_parse.parse_args()

        books = {
            'data': list(map(lambda x: {
                'book_id': x.book_id,
                'book_title': x.book_title,
                'book_description': x.book_description,
                'book_cover': x.book_cover,
                'book_epub': x.book_epub,
                'author': x.author_details.author_name
            },
                             BookDetails.return_by_category(int(data['category_id']), int(data['limit']),
                                                            int(data['page']))))
        }
        return books

top_parse = reqparse.RequestParser()
top_parse.add_argument('limit', type=int, default=10)
top_parse.add_argument('page', type=int, default=1)

class TopBooks(Resource):
    @api.expect(top_parse)
    def get(self):
        data = top_parse.parse_args()
        books = {
            'data': list(map(lambda x: {
                'book_id': x.book_id,
                'book_title': x.book_title,
                'book_cover': x.book_cover,
                'rating': x.get_average_rating()
            },
                             BookDetails.return_top_books(int(data['limit']),
                                                          int(data['page']))))
        }
        return books
        # return BookDetails.return_top_books(int(data['limit']), int(data['page']))

details_parse = reqparse.RequestParser()
details_parse.add_argument('book_id', required=True)
details_parse.add_argument('lang', type=str, choices=('vi', 'en'), default='vi')

class DetailsBook(Resource):
    @api.expect(details_parse)
    def get(self):

        data = details_parse.parse_args()
        v = BookDetails.get_book_details(data['book_id'])
        if not v[0]:
            return 'Book does not exist', 400
        book_details = v[1]
        books = {
            'data': list(map(lambda x: {
                'book_id': x.book_id,
                'book_title': x.book_title,
                'book_description': x.book_description,
                'book_cover': x.book_cover,
                'book_epub': x.book_epub,
                'author': x.author_details.author_name,
                'rating': x.get_average_rating()
            },
                book_details))
        }
        if data["lang"] == "vi":
            book_categories = BookCategories.find_by_book_id(data['book_id'])
            books["data"][0]["categories"] = [CategoryDetails.find_by_id(category.category_id).category_name_vi for category in book_categories]
        else:
            book_categories = BookCategories.find_by_book_id(data['book_id'])
            books["data"][0]["categories"] = [CategoryDetails.find_by_id(category.category_id).category_name_en for
                                              category in book_categories]
        return books, 200

ratings_parse = reqparse.RequestParser()
ratings_parse.add_argument('book_id', required=True)
ratings_parse.add_argument('limit', type=int, default=5)
ratings_parse.add_argument('page', type=int, default=1)

class RatingsBook(Resource):
    @api.expect(ratings_parse)
    def get(self):
        data = ratings_parse.parse_args()
        res = dict()
        res['data'] = []
        v = validate_book_id(data['book_id'])
        if not v[0]:
            return 'Book does not exist', 400
        book_details = v[1]
        rating_details = RatingDetails.find_by_book(book_details.book_id, data['limit'], data['page'])
        for each_rating in rating_details:
            user = UserDetails.find_by_id(each_rating['user_id'])
            each_res = dict()
            each_res['rating_num'] = each_rating['rating_num']
            each_res['rating_comment'] = each_rating['rating_comment']
            each_res['user_name'] = user.user_name
            each_res['full_name'] = refactor_name( user.last_name,  user.first_name)
            each_res['avatar'] = user.avatar
            res['data'].append(each_res)
        return res, 200
