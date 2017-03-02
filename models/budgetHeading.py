from .connection import db


class BudgetHeading(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    initial_amout=db.Column(db.Integer, nullable=False)
    expenses=db.relationship('Expense', backref='budgetHeading', lazy='dynamic')
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'))

    def __init__(self, name=None, initial_amout=None, expenses=[]):
        self.name=name
        self.initial_amout=initial_amout
        self.expenses=expenses

    def __repr__(self):
        return str({'id':self.id, 'name': self.name, 'initial_amoumt': self.initial_amout, 'expenses': self.expenses})