from flask_restful import Resource, reqparse
from models.products import ProductModel


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
        print(productCode)
        product = ProductModel.find_by_productCode(productCode)
        if product:
            return product.json()
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

        if product is None:
            product = ProductModel(productCode, **data)
        else:
            product.productName = data['productName']
            product.productLine = data['productLine']
            product.productScale = data['productScale']
            product.productVendor = data['productVendor']
            product.productDescription = data['productDescription']
            product.quantityInStock = data['quantityInStock']
            product.buyPrice = data['buyPrice']
            product.MSRP = data['MSRP']

        product.save_to_db()

        return {"message": "office alter successful."}


class ProductList(Resource):
    def get(self):
        return {'Products': [product.json() for product in ProductModel.query.all()]}
