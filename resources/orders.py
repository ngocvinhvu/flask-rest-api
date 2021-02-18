from flask_restful import Resource, reqparse
from models.orders import OrderModel


class Orders(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('orderDate',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )

    parser.add_argument('requiredDate',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('shippedDate',
                        type=str,
                        )

    parser.add_argument('status',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('comments',
                        type=str,
                        )

    parser.add_argument('customerNumber',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, orderNumber):
        order = OrderModel.find_by_orderNumber(orderNumber)
        if order:
            return order.json()
        return {'message': 'order not found'}, 404

    def post(self, orderNumber):
        if OrderModel.find_by_orderNumber(orderNumber):
            return {'message': f'A order with orderNumber: {orderNumber} already exists'}, 400

        data = Orders.parser.parse_args()

        order = OrderModel(orderNumber, **data)

        try:
            order.save_to_db()
        except:
            return {"message": "An Error occurred inserting the order."}, 500

        return {"message": "office added successful."}, 201

    def delete(self, orderNumber):

        order = OrderModel.find_by_orderNumber(orderNumber)
        if order:
            order.delete_from_db()
            return {'message': 'order deleted'}
        return {'message': 'Item not found.'}, 404

    def put(self, orderNumber):
        data = Orders.parser.parse_args()

        order = OrderModel.find_by_orderNumber(orderNumber)

        if order is None:
            order = OrderModel(orderNumber, **data)
        else:
            order.orderDate = data['orderDate']
            order.requiredDate = data['requiredDate']
            order.shippedDate = data['shippedDate']
            order.status = data['status']
            order.comments = data['comments']
            order.orderNumber = data['orderNumber']

        order.save_to_db()

        return {"message": "office alter successful."}


class OrderList(Resource):
    def get(self):
        return {'Orders': [order.json() for order in OrderModel.query.all()]}
