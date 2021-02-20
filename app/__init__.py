from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_restful.utils import cors

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    api = Api(app)
    db.init_app(app)
    api.decorators = [cors.crossdomain(origin='*')]

    from app.resources import Customers, CustomerList
    from app.resources import Employees, EmployeeList
    from app.resources import Offices, OfficeList
    from app.resources import Orderdetails, OrderdetailList
    from app.resources import Orders, OrderList
    from app.resources import Payments, PaymentList
    from app.resources import Productlines, ProductlineList
    from app.resources import Products, ProductList

    @app.route('/')
    def index():
        return '<h1>RESTFUL API WEB</h1>'

    api.add_resource(Customers, '/api/v1/customer/<int:customerNumber>')
    api.add_resource(CustomerList, '/api/v1/customers', endpoint='customerlist')

    api.add_resource(Employees, '/api/v1/employee/<int:employeeNumber>')
    api.add_resource(EmployeeList, '/api/v1/employees', endpoint='employeelist')

    api.add_resource(Offices, '/api/v1/office/<int:officeCode>')
    api.add_resource(OfficeList, '/api/v1/offices', endpoint='officelist')

    api.add_resource(Orderdetails, '/api/v1/orderdetail/<string:orderdetailkey>')
    api.add_resource(OrderdetailList, '/api/v1/orderdetails', endpoint='orderdetaillist')

    api.add_resource(Orders, '/api/v1/order/<int:orderNumber>')
    api.add_resource(OrderList, '/api/v1/orders', endpoint='orderlist')

    api.add_resource(Payments, '/api/v1/payment/<int:customerNumber>')
    api.add_resource(PaymentList, '/api/v1/payments', endpoint='paymentlist')

    api.add_resource(Productlines, '/api/v1/productline/<string:productLine>')
    api.add_resource(ProductlineList, '/api/v1/productlines', endpoint='productlinelist')

    api.add_resource(Products, '/api/v1/product/<string:productCode>')
    api.add_resource(ProductList, '/api/v1/products', endpoint='productlist')

    return app
