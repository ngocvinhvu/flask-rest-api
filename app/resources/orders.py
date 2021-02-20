from flask_restful import Resource, reqparse
from app.models.orders import OrderModel
from flask import request, current_app, jsonify, url_for


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

        if order:
            order.delete_from_db()
            order = OrderModel(orderNumber, **data)
        else:
            order = OrderModel(orderNumber, **data)

        order.save_to_db()

        return {"message": "office alter successful."}


class OrderList(Resource):
    def get(self):
        query = request.args
        orders_query = OrderModel.query
        for k, v in query.items():
            if k == 'sort':
                orders_query = orders_query.order_by(v)
            if k == 'customerNumber':
                orders_query = orders_query.filter_by(customerNumber=v)
            if k == 'orderNumber':
                orders_query = orders_query.filter_by(orderNumber=v)

        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', current_app.config['REST_POSTS_PER_PAGE'], type=int)
        pagination = orders_query.paginate(
            page, per_page=limit,
            error_out=False)
        orders = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('orderlist', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('orderlist', page=page + 1)
        return jsonify({
            'orders': [order.json() for order in orders],
            'prev': prev,
            'next': next,
            'Total count': pagination.total,
            'Page count': limit,
        })
