from flask_restful import Resource, reqparse
from models.offices import OfficeModel


class Offices(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('city',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
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
                        type=str
                        )

    parser.add_argument('state',
                        type=str
                        )

    parser.add_argument('country',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('postalCode',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('territory',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, officeCode):
        office = OfficeModel.find_by_officeCode(officeCode)
        if office:
            return office.json()
        return {'message': 'office not found'}, 404

    def post(self, officeCode):
        if OfficeModel.find_by_officeCode(officeCode):
            return {'message': f'A office with officeCode: {officeCode} already exists'}, 400

        data = Offices.parser.parse_args()

        office = OfficeModel(officeCode, **data)

        try:
            office.save_to_db()
        except:
            return {"message": "An Error occurred inserting the office."}, 500

        return {"message": "office added successful."}, 201

    def delete(self, officeCode):

        office = OfficeModel.find_by_officeCode(officeCode)
        if office:
            office.delete_from_db()
            return {'message': 'Office deleted'}
        return {'message': 'Item not found.'}, 204

    def put(self, officeCode):
        data = Offices.parser.parse_args()

        office = OfficeModel.find_by_officeCode(officeCode)

        if office is None:
            office = OfficeModel(officeCode, **data)
        else:
            office.city = data['city']
            office.phone = data['phone']
            office.addressLine1 = data['addressLine1']
            office.addressLine2 = data['addressLine2']
            office.state = data['state']
            office.country = data['country']
            office.postalCode = data['postalCode']
            office.postalCode = data['territory']

        office.save_to_db()

        return {"message": "office alter successful."}


class OfficeList(Resource):
    def get(self):
        return {'offices': list(map(lambda x: x.json(), OfficeModel.query.all()))}
