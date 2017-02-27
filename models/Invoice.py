from .connection import db

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoinscrement=1)
    #Saved invoice as String to get the file (invoice.txt for example)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), Nullable=False)
    invoice = db.Column(db.String(255), Nullable=False)
    def __init__(self, invoice, id):
        self.invoice = invoice
    def __repr__(self):
        return str({
            'id': self.id,
            'invoice': self.invoice
        })