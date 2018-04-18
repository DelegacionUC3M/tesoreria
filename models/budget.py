from .connection import db


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    visibility = db.Column(db.Boolean, nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    budget_headings = db.relationship('BudgetHeading', backref='budget', lazy='dynamic')

    def __init__(self, name, visibility, public, budget_headings=[]):
        self.name = name
        self.visibility = visibility
        self.public = public
        self.budget_headings = budget_headings

    def __repr__(self):
        return str({'id': self.id,
                    'name': self.name,
                    'visibility': self.visibility,
                    'public': self.public,
                    'budget_headings': self.budget_headings})
