from app import db
from models.utils import AddUpdateDelete

class Share(db.Model, AddUpdateDelete):
    __tablename__ = 'share'
    id = db.Column(db.Integer, primary_key=True)
    shareNumber = db.Column(db.Integer)
    dueDate = db.Column(db.DateTime)
    initialBalance = db.Column(db.Float)
    amortization = db.Column(db.Float)
    interest = db.Column(db.Float)
    commission = db.Column(db.Float)
    feeAmount = db.Column(db.Float)
    idLoan = db.Column('idLoan', db.ForeignKey('loan.id'))

    def toJson(self):
        d = {}
        d['idShare'] = self.id
        d['dueDate'] = self.dueDate.strftime('%Y-%m-%d')
        d['initialBalance'] = self.initialBalance
        d['amortization'] = self.amortization
        d['interest'] = self.interest
        d['commission'] = self.commission
        d['feeAmount'] = self.feeAmount
        d['idLoan'] = self.idLoan
        d['shareNumber'] = self.shareNumber

        return d