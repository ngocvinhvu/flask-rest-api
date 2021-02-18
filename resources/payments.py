from flask_restful import Resource, reqparse
from models.payments import PaymentModel


class Payments(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('checkNumber',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )

    parser.add_argument('paymentDate',
                        type=str,
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

        data = payments.parser.parse_args()

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
        data = payments.parser.parse_args()

        payment = PaymentModel.find_by_customerNumber(customerNumber)

        if payment is None:
            payment = PaymentModel(customerNumber, **data)
        else:
            payment.checkNumber = data['checkNumber']
            payment.paymentDate = data['paymentDate']
            payment.amount = data['amount']

        payment.save_to_db()

        return {"message": "office alter successful."}


class PaymentList(Resource):
    def get(self):
        return {'payments': [payment.json() for payment in PaymentModel.query.all()]}
