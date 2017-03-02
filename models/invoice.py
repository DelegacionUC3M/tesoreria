from .connection import db


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #Saved invoice as String to get the file (invoice.txt for example)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), nullable=False)
    invoice = db.Column(db.String(255), nullable=False)

    def __init__(self, invoice, id):
        self.invoice = invoice

    def __repr__(self):
        return str({
            'id': self.id,
            'invoice': self.invoice
        })