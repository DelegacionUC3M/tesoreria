from .connection import db


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budgetheading_id = db.Column(db.Integer, db.ForeignKey('budget_heading.id'))
    name = db.Column(db.String(255), nullable=False)
    school = db.Column(db.Integer, nullable=False)
    expense_date = db.Column(db.DateTime, nullable=False)
    register_date = db.Column(db.DateTime)
    add_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    invoices = db.relationship('Invoice', backref='expense', lazy='dynamic')
    observations = db.Column(db.Text)

    def __init__(self, name, school, expense_date, amount, add_date, revoked, register_date=None, invoices=[], observations=""):
        self.name = name
        self.school = school
        self.expense_date = expense_date
        self.amount = amount
        self.add_date = add_date
        self.revoked = revoked
        self.register_date = register_date
        self.rate = 1 if amount >= 0 else -1
        self.invoices = invoices
        self.observations = observations

    def __repr__(self):
        return str({
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
        })
