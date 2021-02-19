from flask_restful import Resource, reqparse
from app.models.customers import CustomerModel
from flask import request, current_app, jsonify, url_for


class Customers(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('customerName',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )

    parser.add_argument('contactLastName',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('contactFirstName',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('phone',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('addressLine1',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('addressLine2',
                        type=str,
                        )

    parser.add_argument('city',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('state',
                        type=str,
                        )

    parser.add_argument('postalCode',
                        type=str,
                        )

    parser.add_argument('country',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('salesRepEmployeeNumber',
                        type=int,
                        )

    parser.add_argument('creditLimit',
                        type=str,
                        )

    def get(self, customerNumber):
        customer = CustomerModel.find_by_customerNumber(customerNumber)
        if customer:
            return customer.json()
        return {'message': 'customer not found'}, 404

    def post(self, customerNumber):
        if CustomerModel.find_by_customerNumber(customerNumber):
            return {'message': f'A customer with customerNumber: {customerNumber} already exists'}, 400

        data = Customers.parser.parse_args()

        customer = CustomerModel(customerNumber, **data)

        try:
            customer.save_to_db()
        except:
            return {"message": "An Error occurred inserting the customer."}, 500

        return {"message": "office added successful."}, 201

    def delete(self, customerNumber):

        customer = CustomerModel.find_by_customerNumber(customerNumber)
        if customer:
            customer.delete_from_db()
            return {'message': 'customer deleted'}
        return {'message': 'Item not found.'}, 404

    def put(self, customerNumber):
        data = Customers.parser.parse_args()

        customer = CustomerModel.find_by_customerNumber(customerNumber)

        if customer:
            customer.delete_from_db()
            customer = CustomerModel(customerNumber, **data)
        else:
            customer = CustomerModel(customerNumber, **data)

        customer.save_to_db()

        return {"message": "customer alter successful."}


class CustomerList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', current_app.config['REST_POSTS_PER_PAGE'], type=int)
        pagination = CustomerModel.query.paginate(
            page, per_page=limit,
            error_out=False)
        customers = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('customerlist', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('customerlist', page=page + 1)
        return jsonify({
            'customers': [customer.json() for customer in customers],
            'prev': prev,
            'next': next,
            'Total count': pagination.total,
            'Page count': limit,
        })
