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
    record_no_contests = db.Column(db.Integer, default=0)
    weight_class = db.Column(db.String(50))
    ranking = db.Column(db.Integer)
    pound_for_pound_rank = db.Column(db.Integer, nullable=True)
    fights_as_fighter1 = db.relationship('Fight', 
                                       backref='fighter1',
                                       foreign_keys='Fight.fighter1_id',
                                       lazy=True)
    fights_as_fighter2 = db.relationship('Fight', 
                                       backref='fighter2',
                                       foreign_keys='Fight.fighter2_id',
                                       lazy=True)

class Fight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fighter1_id = db.Column(db.Integer, db.ForeignKey('fighter.id'), nullable=False)
    fighter2_id = db.Column(db.Integer, db.ForeignKey('fighter.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    result = db.Column(db.String(200))  # e.g., "Fighter1 via TKO (Round 2)"
    is_title_fight = db.Column(db.Boolean, default=False)
    weight_class = db.Column(db.String(50))
    round = db.Column(db.Integer)
    method = db.Column(db.String(50))  # TKO, Decision, etc.

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    is_upcoming = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)
    fights = db.relationship('Fight', backref='event', lazy=True)