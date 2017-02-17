from .connection import db

class Expense(db.Model):

    id = db.Column(db.Integer, db.ForeignKey('BudgetHeading.id'), primary_key=True, autoincrement=1)
    budgetheading_id = db.Column(db.Integer, db.ForeignKey('budgetheading.id'))
    name = db.Column(db.String(255), Nullable=False)
    school = db.Column(db.Integer, Nullable=False)
    expense_date = db.Column(db.DateTime, Nullable=False)
    register_date = db.Column(db.DateTime, Nullable=False)
    add_date = db.Column(db.DateTime, Nullable=False)
    amount = db.Column(db.Integer, Nullable=False)
    rate = db.Column(db.Integer, Nullable=False)
    revoked = db.Column(db.Boolean, Nullable=False)
    invoices = db.relationship('Invoice', backref='expense',
                            lazy='dynamic')
    observations = db.Column(db.Text, Nullable=False)

def __init__(self, name=None, school=None, expense_date=None, register_date=None, add_date=None, amount=None, revoked=False, invoices=[], observations=None):

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