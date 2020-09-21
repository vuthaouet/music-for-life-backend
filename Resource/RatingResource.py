from flask_restplus import Namespace, Resource, reqparse
from Utils.InputValidation import *
import html


api = Namespace('ratings')


ratings_req = reqparse.RequestParser()
ratings_req.add_argument('limit', type=int, default=5)
ratings_req.add_argument('page', type=int, default=1)

class New(Resource):
    @api.expect(ratings_req)
    def get(self):
        data = ratings_req.parse_args()
        result = RatingDetails.get_new_rating(data["limit"], data["page"])
        ratings = {
            'data': list(map(lambda x: {
                'author_name' : x.author_name,
                'book_id': x.BookDetails.book_id,
                'book_title': x.BookDetails.book_title,
                'book_cover': x.BookDetails.book_cover,
                'user_id': x.UserDetails.user_id,
                'user_name': x.UserDetails.user_name,
                'full_name' : refactor_name( x.UserDetails.last_name,  x.UserDetails.first_name),
                'rating_num': x.RatingDetails.rating_num,
                'rating_comment': x.RatingDetails.rating_comment,
                'created_date': str(x.RatingDetails.created_date)
            },
                             result))
        }
        return ratings



