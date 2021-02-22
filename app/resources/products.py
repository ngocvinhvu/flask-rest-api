from flask_restful import Resource, reqparse
from app.models.products import ProductModel
from flask import request, current_app, jsonify, url_for


class Products(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('productName',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )

    parser.add_argument('productLine',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('productScale',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('productVendor',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('productDescription',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('quantityInStock',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('buyPrice',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('MSRP',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, productCode):
        products = ProductModel.find_by_productCode(productCode)
        if products:
            try:
                return jsonify({'products': [product.json() for product in products]})
            except:
                return products.json()
        return {'message': 'product not found'}, 404

    def post(self, productCode):
        if ProductModel.find_by_productCode(productCode):
            return {'message': f'A product with productCode: {productCode} already exists'}, 400

        data = Products.parser.parse_args()

        product = ProductModel(productCode, **data)

        try:
            product.save_to_db()
        except:
            return {"message": "An Error occurred inserting the product."}, 500

        return {"message": "office added successful."}, 201

    def delete(self, productCode):

        product = ProductModel.find_by_productCode(productCode)
        if product:
            product.delete_from_db()
            return {'message': 'product deleted'}
        return {'message': 'Item not found.'}, 404

    def put(self, productCode):
        data = Products.parser.parse_args()

        product = ProductModel.find_by_productCode(productCode)

        if product:
            product.delete_from_db()
            product = ProductModel(productCode, **data)
        else:
            product = ProductModel(productCode, **data)

        product.save_to_db()

        return {"message": "office alter successful."}


class ProductList(Resource):
    def get(self):
        query = request.args
        products_query = ProductModel.query
        for k, v in query.items():
            if k == 'sort':
                products_query = products_query.order_by(v)
            if k == 'productCode':
                products_query = products_query.filter_by(productCode=v)
            if k == 'productLine':
                products_query = products_query.filter_by(productLine=v)

        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', current_app.config['REST_POSTS_PER_PAGE'], type=int)
        pagination = products_query.paginate(
            page, per_page=limit,
            error_out=False)
        products = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('productlist', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('productlist', page=page + 1)
        return jsonify({
            'products': [product.json() for product in products],
            'prev': prev,
            'next': next,
            'Total count': pagination.total,
            'Page limit': limit,
        })
