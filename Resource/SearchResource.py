from flask_restplus import Namespace, Resource, reqparse
from Utils.InputValidation import *
import html


api = Namespace('search')


search_parse = reqparse.RequestParser()
search_parse.add_argument('text', type=str, default='')
search_parse.add_argument('lang', type=str, choices=('vi', 'en'), default='vi')

class Search(Resource):
    @api.expect(search_parse)
    def get(self):
        data = search_parse.parse_args()
        data['text'] = html.escape(data['text'])
        response = dict()

        books_id = set()
        books_find_by_title = BookDetails.search_by_title(data['text'])
        books_id.update(list(map(lambda x: x.book_id,books_find_by_title)))

        books_find_by_category = CategoryDetails.search_by_category_name(data['text'], data['lang'])
        books_id.update(list(map(lambda x:  x.book_id, books_find_by_category)))

        books_find_by_author = AuthorDetails.search_by_name(data['text'])
        books_id.update(list(map(lambda x:  x.book_id, books_find_by_author)))

        books = []
        for index, id in enumerate(books_id):
            v = BookDetails.get_book_details(id)
            book_details = v[1]
            books += list(map(lambda x: {
                'book_id': x.book_id,
                'book_title': x.book_title,
                'book_cover': x.book_cover,
                'rating' : x.get_average_rating(),
                'author': x.author_details.author_name
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
        return response, 200