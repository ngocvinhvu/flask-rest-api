from flask_restful import Resource, reqparse
from models.orderdetails import OrderdetailModel


class Orderdetails(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('quantityOrdered',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('priceEach',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('orderLineNumber',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, orderdetailkey):
        orderdetail = OrderdetailModel.find_by_orderNumber(orderdetailkey)
        if orderdetail:
            return orderdetail.json()
        else:
            orderdetail = OrderdetailModel.find_by_productCode(orderdetailkey)
            if orderdetail:
                return  orderdetail.json()
            else:
                return {'message': 'orderdetail not found'}, 404

    def post(self, orderdetailkey):
        if OrderdetailModel.find_by_orderNumber(orderdetailkey):
            return {'message': f'A orderdetail with orderNumber: {orderNumber} already exists'}, 400

        if OrderdetailModel.find_by_productCode(orderdetailkey):
            return {'message': f'A orderdetail with productCode: {productCode} already exists'}, 400

        data = Orderdetails.parser.parse_args()

        orderdetail = OrderdetailModel(orderdetailkey, **data)

        try:
            orderdetail.save_to_db()
        except:
            return {"message": "An Error occurred inserting the orderdetail."}, 500

        return {"message": "office added successful."}, 201

    def delete(self, orderdetailkey):
        orderdetail = OrderdetailModel.find_by_orderNumber(orderdetailkey)
        if orderdetail:
            orderdetail.delete_from_db()
            return {'message': 'orderdetail deleted'}
        else:
            orderdetail = OrderdetailModel.find_by_productCode(orderdetailkey)
            if orderdetail:
                orderdetail.delete_from_db()
                return {'message': 'orderdetail deleted'}
            else:
                return {'message': 'orderdetail not found'}, 404

    def put(self, orderdetailkey):
        data = Orderdetails.parser.parse_args()

        orderdetail = OrderdetailModel.find_by_orderNumber(orderdetailkey)
        if orderdetail:
            orderdetail.delete_from_db()
            orderdetail = OrderdetailModel(orderdetailkey, **data)
        else:
            orderdetail = OrderdetailModel.find_by_productCode(orderdetailkey)
            if orderdetail:
                orderdetail.delete_from_db()
                orderdetail = OrderdetailModel(orderdetailkey, **data)
            else:
                orderdetail = OrderdetailModel(orderdetailkey, **data)

        orderdetail.save_to_db()

        return {"message": "office alter successful."}


class OrderdetailList(Resource):
    def get(self):
        return {'Orderdetails': [orderdetail.json() for orderdetail in OrderdetailModel.query.all()]}
