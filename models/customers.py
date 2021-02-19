from db import db


class CustomerModel(db.Model):
    __tablename__ = 'customers'
    customerNumber = db.Column(db.Integer, primary_key=True, nullable=False)
    customerName = db.Column(db.VARCHAR(50), nullable=False)
    contactLastName = db.Column(db.VARCHAR(50), nullable=False)
    contactFirstName = db.Column(db.VARCHAR(50), nullable=False)
    phone = db.Column(db.VARCHAR(50), nullable=False)
    addressLine1 = db.Column(db.VARCHAR(50), nullable=False)
    addressLine2 = db.Column(db.VARCHAR(50), nullable=True)
    city = db.Column(db.VARCHAR(50), nullable=False)
    state = db.Column(db.VARCHAR(50), nullable=True)
    postalCode = db.Column(db.VARCHAR(15), nullable=True)
    country = db.Column(db.VARCHAR(50), nullable=False)
    salesRepEmployeeNumber = db.Column(db.Integer, db.ForeignKey('employees.employeeNumber', ondelete="CASCADE"), index=True, nullable=True)
    creditLimit = db.Column(db.DECIMAL(10, 2), nullable=True)

    order = db.relationship('OrderModel', backref="customers", lazy='dynamic', cascade="all, delete-orphan")
    payment = db.relationship('PaymentModel', backref="customers", lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self,
                 customerNumber,
                 customerName,
                 contactLastName,
                 contactFirstName,
                 phone,
                 addressLine1,
                 addressLine2,
                 city,
                 state,
                 postalCode,
                 country,
                 salesRepEmployeeNumber,
                 creditLimit,
                 ):
        self.customerNumber = customerNumber
        self.customerName = customerName
        self.contactLastName = contactLastName
        self.contactFirstName = contactFirstName
        self.phone = phone
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.city = city
        self.state = state
        self.postalCode = postalCode
        self.country = country
        self.salesRepEmployeeNumber = salesRepEmployeeNumber
        self.creditLimit = creditLimit

    def json(self):
        return {
            "customerNumber": self.customerNumber,
            "customerName": self.customerName,
            "contactLastName": self.contactLastName,
            "contactFirstName": self.contactFirstName,
            "phone": self.phone,
            "addressLine1": self.addressLine1,
            "addressLine2": self.addressLine2,
            "city": self.city,
            "state": self.state,
            "postalCode": self.postalCode,
            "country": self.country,
            "salesRepEmployeeNumber": self.salesRepEmployeeNumber,
            "creditLimit": str(self.creditLimit)
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
