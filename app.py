import os
from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get("SESSION_SECRET")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

@app.route('/')
def index():
    from models import Fighter, Event
    # Get rankings data
    pound_for_pound = Fighter.query.filter(Fighter.pound_for_pound_rank.isnot(None))\
        .order_by(Fighter.pound_for_pound_rank).limit(5).all()

    middleweight_rankings = Fighter.query.filter_by(weight_class='Middleweight')\
        .order_by(Fighter.ranking).limit(10).all()

    lightweight_rankings = Fighter.query.filter_by(weight_class='Lightweight')\
        .order_by(Fighter.ranking).limit(5).all()

    # Get events data
    upcoming_events = Event.query.filter_by(is_upcoming=True)\
        .order_by(Event.date).all()
    past_events = Event.query.filter_by(is_upcoming=False)\
        .order_by(Event.date.desc()).limit(5).all()

    return render_template('index.html',
                         pound_for_pound=pound_for_pound,
                         middleweight_rankings=middleweight_rankings,
                         lightweight_rankings=lightweight_rankings,
                         upcoming_events=upcoming_events,
                         past_events=past_events)

# Create a directory for static files if it doesn't exist
os.makedirs('static/images', exist_ok=True)

# Serve static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

with app.app_context():
    # Import models here to ensure they're registered with SQLAlchemy
    import models  # noqa: F401
    db.create_all()

    # Add some initial data if the database is empty
    from models import Fighter, Event, Fight
    if not Fighter.query.first():
        # Add sample fighters
        fighters = [
            Fighter(name="Luka Kvaskhvadze", record_wins=4, record_losses=0, record_draws=0,
                   weight_class="Middleweight", ranking=1, pound_for_pound_rank=1),
            Fighter(name="Sandro Beroshvili", record_wins=3, record_losses=0, record_draws=0,
                   weight_class="Middleweight", ranking=2, pound_for_pound_rank=2),
            # Add more fighters as needed
        ]
        for fighter in fighters:
            db.session.add(fighter)

        # Add upcoming event
        upcoming_event = Event(
            name="CFN 6: Kvaskhvadze vs. Beroshvili",
            date=datetime(2025, 4, 15),
            is_upcoming=True,
            description="Championship fights!"
        )
        db.session.add(upcoming_event)

        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)