from app import db


class PaymentModel(db.Model):
    __tablename__ = 'payments'
    customerNumber = db.Column(db.Integer, db.ForeignKey('customers.customerNumber', ondelete="CASCADE"), primary_key=True, nullable=False)
    checkNumber = db.Column(db.VARCHAR(50), primary_key=True, nullable=False)
    paymentDate = db.Column(db.Date, nullable=False)
    amount = db.Column(db.DECIMAL(10, 2), nullable=False)

    def __init__(self,
             customerNumber,
             checkNumber,
             paymentDate,
             amount,
             ):
        self.customerNumber = customerNumber
        self.checkNumber = checkNumber
        self.paymentDate = paymentDate
        self.amount = amount

    def json(self):
        return {
            "customerNumber": self.customerNumber,
            "checkNumber": self.checkNumber,
            "paymentDate": str(self.paymentDate),
            "amount": str(self.amount),
        }

    @classmethod
    def find_by_customerNumber(cls, customerNumber):
        return cls.query.filter_by(
            customerNumber=customerNumber
        ).first()

    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()
