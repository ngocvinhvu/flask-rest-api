from db import db


class OrderModel(db.Model):
    __tablename__ = 'orders'
    orderNumber = db.Column(db.Integer, primary_key=True, nullable=False)
    orderDate = db.Column(db.Date, nullable=False)
    requiredDate = db.Column(db.Date, nullable=False)
    shippedDate = db.Column(db.Date, nullable=True)
    status = db.Column(db.VARCHAR(15), nullable=False)
    comments = db.Column(db.Text, nullable=True)
    customerNumber = db.Column(db.Integer, index=True, nullable=False)

    def __init__(self,
             orderNumber,
             orderDate,
             requiredDate,
             shippedDate,
             status,
             comments,
             customerNumber,
             ):
        self.orderNumber = orderNumber
        self.orderDate = orderDate
        self.requiredDate = requiredDate
        self.shippedDate = shippedDate
        self.status = status
        self.comments = comments
        self.customerNumber = customerNumber

    def json(self):
        return {
            "orderNumber": self.orderNumber,
            "orderDate": str(self.orderDate),
            "requiredDate": str(self.requiredDate),
            "shippedDate": str(self.shippedDate),
            "status": self.status,
            "comments": self.comments,
            "customerNumber": self.customerNumber,
        }

    @classmethod
    def find_by_orderNumber(cls, orderNumber):
        return cls.query.filter_by(
            orderNumber=orderNumber
        ).first()

    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()
