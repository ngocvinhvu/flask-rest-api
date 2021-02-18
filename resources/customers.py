from flask_restful import Resource, reqparse
from models.customers import CustomerModel


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

    def patch(self, customerNumber):
        data = Customers.parser.parse_args()

        customer = CustomerModel.find_by_customerNumber(customerNumber)

        if customer is None:
            return {'message': 'Customer not found.'}, 404
        else:
            if 'customerName' in data and customer.customerName != data['customerName']:
                customer.customerName = data['customerName']
            if 'contactLastName' in data and customer.contactLastName != data['contactLastName']:
                customer.contactLastName = data['contactLastName']
            if 'contactFirstName' in data and customer.contactFirstName != data['contactFirstName']:
                customer.contactFirstName = data['contactFirstName']
            if 'phone' in data and customer.phone != data['phone']:
                customer.phone = data['phone']
            if 'addressLine1' in data and customer.addressLine1 != data['addressLine1']:
                customer.addressLine1 = data['addressLine1']
            if 'addressLine2' in data and customer.addressLine2 != data['addressLine2']:
                customer.addressLine2 = data['addressLine2']
            if 'city' in data and customer.city != data['city']:
                customer.city = data['city']
            if 'state' in data and customer.state != data['state']:
                customer.state = data['state']
            if 'postalCode' in data and customer.postalCode != data['postalCode']:
                customer.postalCode = data['postalCode']
            if 'country' in data and customer.country != data['country']:
                customer.country = data['country']
            if 'salesRepEmployeeNumber' in data and customer.salesRepEmployeeNumber != data['salesRepEmployeeNumber']:
                customer.salesRepEmployeeNumber = data['salesRepEmployeeNumber']
            if 'creditLimit' in data and customer.creditLimit != data['creditLimit']:
                customer.creditLimit = data['creditLimit']
        customer.save_to_db()

        return {"message": "customer updated successful."}

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
        return {'Customers': [customer.json() for customer in CustomerModel.query.all()]}
