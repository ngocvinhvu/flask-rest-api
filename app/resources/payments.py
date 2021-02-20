from flask_restful import Resource, reqparse
from app.models.payments import PaymentModel
from flask import request, current_app, jsonify, url_for
from datetime import datetime


class Payments(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('checkNumber',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )

    parser.add_argument('paymentDate',
                        type=lambda d: datetime.strptime(d, '%Y-%m-%d').astimezone().replace(microsecond=0).isoformat(),
                        required=True,
                        help="This field cannot be left blank"
                        )

    parser.add_argument('amount',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, customerNumber):
        payment = PaymentModel.find_by_customerNumber(customerNumber)
        if payment:
            return payment.json()
        return {'message': 'payment not found'}, 404

    def post(self, customerNumber):
        if PaymentModel.find_by_customerNumber(customerNumber):
            return {'message': f'A payment with customerNumber: {customerNumber} already exists'}, 400

        data = Payments.parser.parse_args()

        payment = PaymentModel(customerNumber, **data)

        try:
            payment.save_to_db()
        except:
            return {"message": "An Error occurred inserting the payment."}, 500

        return {"message": "office added successful."}, 201

    def delete(self, customerNumber):

        payment = PaymentModel.find_by_customerNumber(customerNumber)
        if payment:
            payment.delete_from_db()
            return {'message': 'payment deleted'}
        return {'message': 'Item not found.'}, 404

    def put(self, customerNumber):
        data = Payments.parser.parse_args()

        payment = PaymentModel.find_by_customerNumber(customerNumber)

        if payment:
            payment.delete_from_db()
            payment = PaymentModel(customerNumber, **data)
        else:
            payment = PaymentModel(customerNumber, **data)

        payment.save_to_db()

        return {"message": "office alter successful."}


class PaymentList(Resource):
    def get(self):
        query = request.args
        payments_query = PaymentModel.query
        for k, v in query.items():
            if k == 'sort':
                payments_query = payments_query.order_by(v)
            if k == 'customerNumber':
                payments_query = payments_query.filter_by(customerNumber=v)
            if k == 'paymentDate':
                payments_query = payments_query.filter_by(paymentDate=v)

        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', current_app.config['REST_POSTS_PER_PAGE'], type=int)
        pagination = payments_query.paginate(
            page, per_page=limit,
            error_out=False)
        payments = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('paymentlist', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('paymentlist', page=page + 1)
        return jsonify({
            'payments': [payment.json() for payment in payments],
            'prev': prev,
            'next': next,
            'Total count': pagination.total,
            'Page count': limit,
        })
