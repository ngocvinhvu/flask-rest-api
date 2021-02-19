from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    api = Api(app)
    db.init_app(app)

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

    api.add_resource(Customers, '/customer/<int:customerNumber>')
    api.add_resource(CustomerList, '/customers', endpoint='customerlist')

    api.add_resource(Employees, '/employee/<int:employeeNumber>')
    api.add_resource(EmployeeList, '/employees', endpoint='employeelist')

    api.add_resource(Offices, '/office/<int:officeCode>')
    api.add_resource(OfficeList, '/offices', endpoint='officelist')

    api.add_resource(Orderdetails, '/orderdetail/<string:orderdetailkey>')
    api.add_resource(OrderdetailList, '/orderdetails', endpoint='orderdetaillist')

    api.add_resource(Orders, '/order/<int:orderNumber>')
    api.add_resource(OrderList, '/orders', endpoint='orderlist')

    api.add_resource(Payments, '/payment/<int:customerNumber>')
    api.add_resource(PaymentList, '/payments', endpoint='paymentlist')

    api.add_resource(Productlines, '/productline/<string:productLine>')
    api.add_resource(ProductlineList, '/productlines', endpoint='productlinelist')

    api.add_resource(Products, '/product/<string:productCode>')
    api.add_resource(ProductList, '/products', endpoint='productlist')

    return app
