from app import db
from datetime import datetime

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Fighter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    record_wins = db.Column(db.Integer, default=0)
    record_losses = db.Column(db.Integer, default=0)
    record_draws = db.Column(db.Integer, default=0)
    weight_class = db.Column(db.String(50))
    ranking = db.Column(db.Integer)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    is_upcoming = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)
