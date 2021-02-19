from flask import Flask
from flask_restful import Api
from resources.customers import Customers, CustomerList
from resources.employees import Employees, EmployeeList
from resources.offices import Offices, OfficeList
from resources.orderdetails import Orderdetails, OrderdetailList
from resources.orders import Orders, OrderList
from resources.payments import Payments, PaymentList
from resources.productlines import Productlines, ProductlineList
from resources.products import Products, ProductList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tris:trianh1998@localhost/classicmodels'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REST_POSTS_PER_PAGE'] = 25

api = Api(app)

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

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
