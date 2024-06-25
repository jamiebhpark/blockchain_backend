# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    ethereum_address = db.Column(db.String(120), unique=True, nullable=False)
    assets = db.Column(db.Float, default=1000.0)


class Transaction(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    receiver = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    txn_hash = db.Column(db.String(120), nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat(),
            "txn_hash": self.txn_hash
        }
