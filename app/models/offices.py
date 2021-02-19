from app import db


class OfficeModel(db.Model):
    __tablename__ = 'offices'
    officeCode = db.Column(db.VARCHAR(10), primary_key=True, nullable=False)
    city = db.Column(db.VARCHAR(50), nullable=False)
    phone = db.Column(db.VARCHAR(50), nullable=False)
    addressLine1 = db.Column(db.VARCHAR(50), nullable=False)
    addressLine2 = db.Column(db.VARCHAR(50), nullable=True)
    state = db.Column(db.VARCHAR(50), nullable=True)
    country = db.Column(db.VARCHAR(50), nullable=False)
    postalCode = db.Column(db.VARCHAR(15), nullable=False)
    territory = db.Column(db.VARCHAR(10), nullable=False)

    employee = db.relationship('EmployeeModel', backref='offices', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self,
                 officeCode,
                 city,
                 phone,
                 addressLine1,
                 addressLine2,
                 state,
                 country,
                 postalCode,
                 territory,
                 ):
        self.officeCode = officeCode
        self.city = city
        self.phone = phone
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.state = state
        self.country = country
        self.postalCode = postalCode
        self.territory = territory

    def json(self):
        return {
            "officeCode": self.officeCode,
            "city": self.city,
            "phone": self.phone,
            "addressLine1": self.addressLine1,
            "addressLine2": self.addressLine2,
            "state": self.state,
            "country": self.country,
            "postalCode": self.postalCode,
            "territory": self.territory
        }

    @classmethod
    def find_by_officeCode(cls, officeCode):
        return cls.query.filter_by(
            officeCode=officeCode
        ).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
