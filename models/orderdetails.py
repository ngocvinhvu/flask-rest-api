from db import db


class OrderdetailModel(db.Model):
    __tablename__ = 'orderdetails'
    orderNumber = db.Column(db.Integer, primary_key=True, nullable=False, db.ForeignKey('orders.orderNumber'))
    productCode = db.Column(db.VARCHAR(15), primary_key=True, index=True, nullable=False, db.ForeignKey('products.productCode'))
    quantityOrdered = db.Column(db.Integer, nullable=False)
    priceEach = db.Column(db.DECIMAL(10, 2), nullable=False)
    orderLineNumber = db.Column(db.SMALLINT, nullable=False)

    def __init__(self,
             orderNumber,
             productCode,
             quantityOrdered,
             priceEach,
             orderLineNumber,
             ):
        self.orderNumber = orderNumber
        self.productCode = productCode
        self.quantityOrdered = quantityOrdered
        self.priceEach = priceEach
        self.orderLineNumber = orderLineNumber

    def json(self):
        return {
            "orderNumber": self.orderNumber,
            "productCode": self.productCode,
            "quantityOrdered": self.quantityOrdered,
            "priceEach": str(self.priceEach),
            "orderLineNumber": self.orderLineNumber,
        }

    @classmethod
    def find_by_orderNumber(cls, orderNumber):
        return cls.query.filter_by(
            orderNumber=orderNumber
        ).first()

    @classmethod
    def find_by_productCode(cls, productCode):
        return cls.query.filter_by(
            productCode=productCode
        ).first()

    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()
