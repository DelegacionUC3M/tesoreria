from .connection import db
from models import Invoice

class Expense(db.Model):

    id = db.Column(db.Integer, db.ForeignKey('BudgetHeading.id'), primary_key=True, autoincrement=1)
    budgetheading_id = db.Column(db.Integer, db.ForeignKey('budgetheading.id'))
    name = db.Column(db.String(255))
    school = db.Column(db.Integer)
    expense_date = db.Column(db.DateTime)
    register_date = db.Column(db.DateTime)
    add_date = db.Column(db.DateTime)
    amount = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    revoked = db.Column(db.Boolean)
    invoices = db.relationship('Invoice', backref='expense',
                            lazy='dynamic')
    observations = db.Column(db.Text)

def __init__(self, id, name, school, expense_date, register_date, add_date, amount, revoked, invoices, observations):

    self.id = id
    self.name = name
    self.school = school
    self.expense_date = expense_date
    self.register_date = register_date
    self.add_date = add_date
    self.amount = amount
    if(amount >= 0):
        self.rate = 1
    else:
        self.rate = -1
    self.revoked = revoked
    self.invoices = invoices
    self.observations = observations

def __repr__(self):

    return{
        'id': self.id,
        'name': self.name,
        'school': self.school,
        'expense_date': self.expense_date,
        'register_date': self.register_date,
        'add_date': self.add_date,
        'amount': self.amount,
        'rate': self.rate,
        'revoked': self.revoked,
        'invoices': self.invoices,
        'observations': self.observations
    }