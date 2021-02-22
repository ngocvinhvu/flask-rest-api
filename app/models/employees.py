from app import db


class EmployeeModel(db.Model):
    __tablename__ = 'employees'
    employeeNumber = db.Column(db.Integer, primary_key=True, nullable=False)
    lastName = db.Column(db.VARCHAR(50), nullable=False)
    firstName = db.Column(db.VARCHAR(50), nullable=False)
    extension = db.Column(db.VARCHAR(10), nullable=False)
    email = db.Column(db.VARCHAR(100), nullable=False)
    officeCode = db.Column(db.VARCHAR(10), db.ForeignKey('offices.officeCode', ondelete="CASCADE"), index=True, nullable=False)
    reportsTo = db.Column(db.Integer, db.ForeignKey('employees.employeeNumber', ondelete="CASCADE"), nullable=True, index=True)
    jobTitle = db.Column(db.VARCHAR(50), nullable=False)

    employee = db.relationship("EmployeeModel", remote_side=[employeeNumber], cascade='all, delete-orphan', single_parent=True)

    def __init__(self,
                 employeeNumber,
                 lastName,
                 firstName,
                 extension,
                 email,
                 officeCode,
                 reportsTo,
                 jobTitle,
                 ):
        self.employeeNumber = employeeNumber
        self.lastName = lastName
        self.firstName = firstName
        self.extension = extension
        self.email = email
        self.officeCode = officeCode
        self.reportsTo = reportsTo
        self.jobTitle = jobTitle

    def json(self):
        return {
            "employeeNumber": self.employeeNumber,
            "lastName": self.lastName,
            "firstName": self.firstName,
            "extension": self.extension,
            "email": self.email,
            "officeCode": self.officeCode,
            "reportsTo": self.reportsTo,
            "jobTitle": self.jobTitle
        }

    @classmethod
    def find_by_employeeNumber(cls, employeeNumber):
        return cls.query.filter_by(
            employeeNumber=employeeNumber
        ).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
