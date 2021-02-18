from flask_restful import Resource, reqparse
from models.employees import EmployeeModel


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

    def patch(self, employeeNumber):
        data = Employees.parser.parse_args()

        employee = EmployeeModel.find_by_employeeNumber(employeeNumber)

        if employee is None:
            return {'message': 'Employee not found.'}, 404
        else:
            if 'lastName' in data and employee.lastName != data['lastName']:
                employee.lastName = data['lastName']
            if 'firstName' in data and employee.firstName != data['firstName']:
                employee.firstName = data['firstName']
            if 'extension' in data and employee.extension != data['extension']:
                employee.extension = data['extension']
            if 'email' in data and employee.email != data['email']:
                employee.email = data['email']
            if 'officeCode' in data and employee.officeCode != data['officeCode']:
                employee.officeCode = data['officeCode']
            if 'reportsTo' in data and employee.reportsTo != data['reportsTo']:
                employee.reportsTo = data['reportsTo']
            if 'jobTitle' in data and employee.jobTitle != data['jobTitle']:
                employee.jobTitle = data['jobTitle']

        employee.save_to_db()

        return {"message": "employee updated successful."}

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
        return {'employees': [employee.json() for employee in EmployeeModel.query.all()]}
