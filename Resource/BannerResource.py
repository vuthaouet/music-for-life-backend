from flask_restplus import Namespace, Resource, reqparse
from Utils.InputValidation import *
import html


api = Namespace('banner')


banner_req = reqparse.RequestParser()
banner_req.add_argument('limit', type=int, default=5)
banner_req.add_argument('page', type=int, default=1)

class All(Resource):
    @api.expect(banner_req)
    def get(self):
        data = banner_req.parse_args()
        result = BannerDetails.return_all(data["limit"], data["page"])
        return result



