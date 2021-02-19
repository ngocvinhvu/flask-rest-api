from flask_restful import Resource, reqparse
from flask.app.models import EmployeeModel
from flask import request, current_app, jsonify, url_for


class Employees(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('lastName',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('firstName',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('extension',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('officeCode',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('reportsTo',
                        type=int,
                        )

    parser.add_argument('jobTitle',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, employeeNumber):
        employee = EmployeeModel.find_by_employeeNumber(employeeNumber)
        if employee:
            return employee.json()
        return {'message': 'employee not found'}, 404

    def post(self, employeeNumber):
        if EmployeeModel.find_by_employeeNumber(employeeNumber):
            return {'message': f'A employee with employeeNumber: {employeeNumber} already exists'}, 400

        data = Employees.parser.parse_args()

        employee = EmployeeModel(employeeNumber, **data)

        try:
            employee.save_to_db()
        except:
            return {"message": "An Error occurred inserting the employee."}, 500

        return {"message": "office added successful."}, 201

    def delete(self, employeeNumber):
        employee = EmployeeModel.find_by_employeeNumber(employeeNumber)
        if employee:
            employee.delete_from_db()
            return {'message': 'employee deleted'}
        return {'message': 'Item not found.'}, 404

    def put(self, employeeNumber):
        data = Employees.parser.parse_args()

        employee = EmployeeModel.find_by_employeeNumber(employeeNumber)

        if employee:
            employee.delete_from_db()
            employee = EmployeeModel(employeeNumber, **data)
        else:
            employee = EmployeeModel(employeeNumber, **data)

        employee.save_to_db()

        return {"message": "employee alter successful."}


class EmployeeList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', current_app.config['REST_POSTS_PER_PAGE'], type=int)
        pagination = EmployeeModel.query.paginate(
            page, per_page=limit,
            error_out=False)
        employees = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('employeelist', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('employeelist', page=page + 1)
        return jsonify({
            'employees': [employee.json() for employee in employees],
            'prev': prev,
            'next': next,
            'Total count': pagination.total,
            'Page count': limit,
        })
