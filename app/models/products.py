from app import db


class ProductModel(db.Model):
    __tablename__ = 'products'
    productCode = db.Column(db.VARCHAR(15), primary_key=True, nullable=False)
    productName = db.Column(db.VARCHAR(70), nullable=False)
    productLine = db.Column(db.VARCHAR(50), db.ForeignKey('productlines.productLine', ondelete="CASCADE"), nullable=False, index=True)
    productScale = db.Column(db.VARCHAR(10), nullable=False)
    productVendor = db.Column(db.VARCHAR(50), nullable=False)
    productDescription = db.Column(db.Text, nullable=False)
    quantityInStock = db.Column(db.SMALLINT, nullable=False)
    buyPrice = db.Column(db.DECIMAL(10, 2), nullable=False)
    MSRP = db.Column(db.DECIMAL(10, 2), nullable=False)

    orderdetail = db.relationship('OrderdetailModel', backref='products', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self,
             productCode,
             productName,
             productLine,
             productScale,
             productVendor,
             productDescription,
             quantityInStock,
             buyPrice,
             MSRP,
             ):
        self.productCode = productCode
        self.productName = productName
        self.productLine = productLine
        self.productScale = productScale
        self.productVendor = productVendor
        self.productDescription = productDescription
        self.quantityInStock = quantityInStock
        self.buyPrice = buyPrice
        self.MSRP = MSRP

    def json(self):
        return {
            "productCode": self.productCode,
            "productName": self.productName,
            "productLine": self.productLine,
            "productScale": self.productScale,
            "productVendor": self.productVendor,
            "productDescription": self.productDescription,
            "quantityInStock": self.quantityInStock,
            "buyPrice": str(self.buyPrice),
            "MSRP": str(self.MSRP),
        }

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
