from flask_restful import Resource, reqparse
from app.models.offices import OfficeModel
from flask import request, current_app, jsonify, url_for


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

        if office:
            office.delete_from_db()
            office = OfficeModel(officeCode, **data)
        else:
            office = OfficeModel(officeCode, **data)

        office.save_to_db()

        return {"message": "office alter successful."}


class OfficeList(Resource):
    def get(self):
        query = request.args
        offices_query = OfficeModel.query
        for k, v in query.items():
            if k == 'sort':
                offices_query = offices_query.order_by(v)
            if k == 'country':
                offices_query = offices_query.filter_by(country=v)
            if k == 'city':
                offices_query = offices_query.filter_by(city=v)

        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', current_app.config['REST_POSTS_PER_PAGE'], type=int)
        pagination = offices_query.paginate(
            page, per_page=limit,
            error_out=False)
        offices = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('officelist', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('officelist', page=page + 1)
        return jsonify({
            'offices': [office.json() for office in offices],
            'prev': prev,
            'next': next,
            'Total count': pagination.total,
            'Page count': limit,
        })
