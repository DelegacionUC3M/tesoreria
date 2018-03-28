from .connection import db


class BudgetHeading(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'))
    name = db.Column(db.String(255), nullable=False)
    initial_amount = db.Column(db.Integer, nullable=False)
    expenses = db.relationship('Expense', backref='budgetHeading', lazy='dynamic')

    def __init__(self, budget_id, name, initial_amout, expenses=[]):
        self.budget_id=budget_id
        self.name = name
        self.initial_amout = initial_amout
        self.expenses = expenses

    def __repr__(self):
        return str({'id': self.id, 'name': self.name, 'initial_amoumt': self.initial_amout, 'expenses': self.expenses})
