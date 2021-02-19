from flask_restful import Resource, reqparse
from models.productlines import ProductlineModel
from flask import request, current_app, jsonify, url_for


class Productlines(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('textDescription',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )

    parser.add_argument('htmlDescription',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )

    parser.add_argument('image',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, productLine):
        productline = ProductlineModel.find_by_productLine(productLine)
        if productline:
            return productline.json()
        return {'message': 'productline not found'}, 404

    def post(self, productLine):
        if ProductlineModel.find_by_productLine(productLine):
            return {'message': f'A productline with productLine: {productLine} already exists'}, 400

        data = Productlines.parser.parse_args()

        productline = ProductlineModel(productLine, **data)

        try:
            productline.save_to_db()
        except:
            return {"message": "An Error occurred inserting the productline."}, 500

        return {"message": "office added successful."}, 201

    def delete(self, productLine):

        productline = ProductlineModel.find_by_productLine(productLine)
        if productline:
            productline.delete_from_db()
            return {'message': 'productline deleted'}
        return {'message': 'Item not found.'}, 404

    def put(self, productLine):
        data = Productlines.parser.parse_args()

        productline = ProductlineModel.find_by_productLine(productLine)

        if productline:
            productline.delete_from_db()
            productline = ProductlineModel(productLine, **data)
        else:
            productline = ProductlineModel(productLine, **data)

        productline.save_to_db()

        return {"message": "office alter successful."}


class ProductlineList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = ProductlineModel.query.paginate(
            page, per_page=current_app.config['REST_POSTS_PER_PAGE'],
            error_out=False)
        productlines = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('productlinelist', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('productlinelist', page=page + 1)
        return jsonify({
            'productlines': [productline.json() for productline in productlines],
            'prev': prev,
            'next': next,
            'Total count': pagination.total,
            'Page count': current_app.config['REST_POSTS_PER_PAGE'],
        })
