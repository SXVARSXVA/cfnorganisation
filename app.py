import os
from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
app.config["SQLALCHEMY_ECHO"] = True  # Enable SQL query logging

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401

    db.create_all()

@app.route('/')
def index():
    from models import Fighter, Event, Fight
    # Get rankings data
    pound_for_pound = Fighter.query.filter(Fighter.pound_for_pound_rank.isnot(None))\
        .order_by(Fighter.pound_for_pound_rank).all()

    middleweight_rankings = Fighter.query.filter_by(weight_class='Middleweight')\
        .order_by(Fighter.ranking).all()

    lightweight_rankings = Fighter.query.filter_by(weight_class='Lightweight')\
        .order_by(Fighter.ranking).all()

    # Get events data
    upcoming_events = Event.query.filter_by(is_upcoming=True)\
        .order_by(Event.date).all()
    past_events = Event.query.filter_by(is_upcoming=False)\
        .order_by(Event.date.desc()).all()

    # Create a set of all fighters for profiles
    all_fighters = list(set(pound_for_pound + middleweight_rankings + lightweight_rankings))

    return render_template('index.html',
                         pound_for_pound=pound_for_pound,
                         middleweight_rankings=middleweight_rankings,
                         lightweight_rankings=lightweight_rankings,
                         upcoming_events=upcoming_events,
                         past_events=past_events,
                         all_fighters=all_fighters)

# Create directories for static files if they don't exist
os.makedirs('static/images', exist_ok=True)

# Serve static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

with app.app_context():
    # Import models here to ensure they're registered with SQLAlchemy
    from models import Fighter, Event, Fight

    # Add initial data if the database is empty
    if not Fighter.query.first():
        # Add fighters with complete records
        fighters = {
            "Luka Kvaskhvadze": {"wins": 4, "losses": 0, "draws": 0, "weight_class": "Middleweight", "ranking": 1, "p4p": 1},
            "Sandro Beroshvili": {"wins": 3, "losses": 0, "draws": 0, "weight_class": "Middleweight", "ranking": 2, "p4p": 2},
            "Nika Berulava": {"wins": 2, "losses": 0, "draws": 0, "weight_class": "Lightweight", "ranking": 1, "p4p": 3},
            "Nika Beroshvili": {"wins": 1, "losses": 0, "draws": 1, "weight_class": "Middleweight", "ranking": 3, "p4p": 4},
            "Levan Totochia": {"wins": 1, "losses": 0, "draws": 0, "weight_class": "Middleweight", "ranking": 4, "p4p": 5},
            "Sandro Datiashvili": {"wins": 1, "losses": 1, "draws": 1, "weight_class": "Middleweight", "ranking": 5},
            "Giorgi Bukhrashvili": {"wins": 0, "losses": 1, "draws": 0, "weight_class": "Middleweight", "ranking": 6},
            "Giorgi Kiladze": {"wins": 0, "losses": 1, "draws": 0, "weight_class": "Middleweight", "ranking": 7},
            "Gigi Kenkishvili": {"wins": 0, "losses": 1, "draws": 0, "weight_class": "Middleweight", "ranking": 8},
            "Rezi Gagua": {"wins": 0, "losses": 1, "draws": 0, "weight_class": "Middleweight", "ranking": 9, "no_contests": 1},
            "Saba Zathiashvili": {"wins": 0, "losses": 1, "draws": 0, "weight_class": "Middleweight", "ranking": 10},
            "Saba Kasradze": {"wins": 1, "losses": 0, "draws": 0, "weight_class": "Lightweight", "ranking": 2},
            "Luka Javakhishvili": {"wins": 1, "losses": 1, "draws": 0, "weight_class": "Lightweight", "ranking": 3},
            "Sandro Chalashvili": {"wins": 0, "losses": 2, "draws": 0, "weight_class": "Lightweight", "ranking": 4},
            "Misho Keshelava": {"wins": 0, "losses": 1, "draws": 0, "weight_class": "Lightweight", "ranking": 5},
            "Viktor Tskhvaradze": {"wins": 0, "losses": 0, "draws": 0, "weight_class": "Lightweight", "ranking": 6},
            "Nika Antadze": {"wins": 0, "losses": 0, "draws": 0, "weight_class": "Middleweight", "ranking": 11},
            "Demetre Tabatadze": {"wins":2, "losses":1, "draws":0, "weight_class": "Lightweight", "ranking": 7},
            "Lado Jariashvili": {"wins":0, "losses":2, "draws":0, "weight_class": "Lightweight", "ranking": 8},
            "Nika Chartia": {"wins":0, "losses":1, "draws":0, "weight_class": "Middleweight", "ranking": 12},
            "Giorgi Chanadiri": {"wins":0, "losses":1, "draws":0, "weight_class": "Middleweight", "ranking": 13},
            "Nikoloz Jirkmelishvili": {"wins":0, "losses":1, "draws":0, "weight_class": "Middleweight", "ranking": 14},
            "Nika Metreveli": {"wins":0, "losses":0, "draws":0, "weight_class": "Middleweight", "ranking": 15}
        }

        fighter_objects = {}
        for name, data in fighters.items():
            fighter = Fighter(
                name=name,
                record_wins=data["wins"],
                record_losses=data["losses"],
                record_draws=data["draws"],
                record_no_contests=data.get("no_contests", 0),
                weight_class=data["weight_class"],
                ranking=data["ranking"],
                pound_for_pound_rank=data.get("p4p")
            )
            db.session.add(fighter)
            fighter_objects[name] = fighter

        # Add upcoming event
        cfn6 = Event(
            name="CFN 6: Kvaskhvadze vs. Beroshvili",
            date=datetime(2025, 4, 15),
            is_upcoming=True,
            description="Two Championship Fights!"
        )
        db.session.add(cfn6)

        # Add past events with complete fight history
        past_events = [
            {
                "name": "CFN 5",
                "date": datetime(2024, 12, 15),
                "fights": [
                    # Main Card
                    {"fighter1": "Luka Kvaskhvadze", "fighter2": "Nika Chartia", 
                     "result": "Kvaskhvadze Wins via TKO in Round 1", "weight_class": "Middleweight", "is_main_card": True},
                    {"fighter1": "Sandro Beroshvili", "fighter2": "Giorgi Bukhrashvili",
                     "result": "Beroshvili Wins via TKO in Round 4", "weight_class": "Middleweight", "is_main_card": True},
                    {"fighter1": "Levan Totochia", "fighter2": "Saba Zathiashvili",
                     "result": "Totochia Wins via TKO in Round 1", "weight_class": "Middleweight", "is_main_card": True},
                     
                    # Preliminary Card
                    {"fighter1": "Saba Kasradze", "fighter2": "Demetre Tabatadze",
                     "result": "Kasradze Wins via TKO in Round 3", "weight_class": "Lightweight", "is_main_card": False},
                    {"fighter1": "Nika Berulava", "fighter2": "Misho Keshelava",
                     "result": "Berulava Wins via TKO in Round 2", "weight_class": "Lightweight", "is_main_card": False},
                    {"fighter1": "Nika Beroshvili", "fighter2": "Nika Metreveli",
                     "result": "Cancelled", "weight_class": "Middleweight", "is_main_card": False}
                ]
            },
            {
                "name": "CFN 4",
                "date": datetime(2024, 9, 1),
                "fights": [
                    # Main Card
                    {"fighter1": "Luka Javakhishvili", "fighter2": "Sandro Chalashvili",
                     "result": "Javakhishvili Wins via TKO in Round 3", "weight_class": "Lightweight", "is_main_card": True},
                    {"fighter1": "Sandro Datiashvili", "fighter2": "Rezi Gagua",
                     "result": "Datiashvili Wins via TKO in Round 3", "weight_class": "Middleweight", "is_main_card": True},
                     
                    # Preliminary Card
                    {"fighter1": "Sandro Beroshvili", "fighter2": "Gigi Kenkishvili",
                     "result": "Beroshvili Wins via TKO in Round 3", "weight_class": "Middleweight", "is_main_card": False},
                    {"fighter1": "Nika Berulava", "fighter2": "Misho Keshelava",
                     "result": "Cancelled", "weight_class": "Lightweight", "is_main_card": False}
                ]
            },
            {
                "name": "CFN 3",
                "date": datetime(2024, 6, 1),
                "fights": [
                    # Main Card
                    {"fighter1": "Luka Kvaskhvadze", "fighter2": "Nikoloz Jirkmelishvili",
                     "result": "Kvaskhvadze Wins via TKO in Round 4", "weight_class": "Middleweight", "is_main_card": True},
                     
                    # Preliminary Card
                    {"fighter1": "Demetre Tabatadze", "fighter2": "Lado Jariashvili",
                     "result": "Tabatadze Wins via doctor stoppage in Round 2", "weight_class": "Lightweight", "is_main_card": False},
                    {"fighter1": "Nika Berulava", "fighter2": "Luka Javakhishvili",
                     "result": "Berulava Wins via TKO in Round 3", "weight_class": "Lightweight", "is_main_card": False}
                ]
            },
            {
                "name": "CFN 2",
                "date": datetime(2024, 3, 1),
                "fights": [
                    # Main Card
                    {"fighter1": "Luka Kvaskhvadze", "fighter2": "Giorgi Kiladze",
                     "result": "Kvaskhvadze Wins via TKO in Round 3", "weight_class": "Middleweight", "is_main_card": True},
                    {"fighter1": "Nika Beroshvili", "fighter2": "Sandro Datiashvili",
                     "result": "Beroshvili Wins via Unanimous Decision", "weight_class": "Middleweight", "is_main_card": True},
                     
                    # Preliminary Card
                    {"fighter1": "Demetre Tabatadze", "fighter2": "Lado Jariashvili",
                     "result": "Tabatadze Wins via doctor stoppage in Round 2", "weight_class": "Lightweight", "is_main_card": False},
                    {"fighter1": "Sandro Beroshvili", "fighter2": "Giorgi Chanadiri",
                     "result": "Beroshvili Wins via TKO in Round 1", "weight_class": "Middleweight", "is_main_card": False}
                ]
            },
            {
                "name": "CFN 1",
                "date": datetime(2023, 12, 1),
                "fights": [
                    # Main Card
                    {"fighter1": "Luka Kvaskhvadze", "fighter2": "Sandro Chalashvili",
                     "result": "Kvaskhvadze Wins via TKO in Round 1", "weight_class": "Lightweight", "is_main_card": True},
                    {"fighter1": "Nika Metreveli", "fighter2": "Rezi Gagua",
                     "result": "No Contest", "weight_class": "Middleweight", "is_main_card": True},
                     
                    # Preliminary Card
                    {"fighter1": "Demetre Tabatadze", "fighter2": "Lado Jariashvili",
                     "result": "Cancelled", "weight_class": "Lightweight", "is_main_card": False},
                    {"fighter1": "Nika Beroshvili", "fighter2": "Sandro Datiashvili",
                     "result": "Draw", "weight_class": "Middleweight", "is_main_card": False}
                ]
            }
        ]

        for event_data in past_events:
            event = Event(
                name=event_data["name"],
                date=event_data["date"],
                is_upcoming=False
            )
            db.session.add(event)

            for fight_data in event_data["fights"]:
                if fight_data["fighter1"] in fighter_objects and fight_data["fighter2"] in fighter_objects:
                    fight = Fight(
                        fighter1=fighter_objects[fight_data["fighter1"]],
                        fighter2=fighter_objects[fight_data["fighter2"]],
                        result=fight_data["result"],
                        weight_class=fight_data["weight_class"],
                        is_main_card=fight_data.get("is_main_card", True),  # Default to main card if not specified
                        event=event
                    )
                    db.session.add(fight)

        # Add CFN 6 fights
        event = Event.query.filter_by(name="CFN 6: Kvaskhvadze vs. Beroshvili").first()
        if event:
            # Main Event - Middleweight Championship
            luka = Fighter.query.filter_by(name="Luka Kvaskhvadze").first()
            sandro = Fighter.query.filter_by(name="Sandro Beroshvili").first()
            if luka and sandro:
                fight = Fight(
                    fighter1=luka,
                    fighter2=sandro,
                    event=event,
                    is_title_fight=True,
                    weight_class="Middleweight"
                )
                db.session.add(fight)

            # Co-Main Event - Lightweight Championship
            nika = Fighter.query.filter_by(name="Nika Berulava").first()
            viktor = Fighter.query.filter_by(name="Viktor Tskhvaradze").first()
            if nika and viktor:
                fight = Fight(
                    fighter1=nika,
                    fighter2=viktor,
                    event=event,
                    is_title_fight=True,
                    weight_class="Lightweight"
                )
                db.session.add(fight)

            # Preliminary Card
            nika_b = Fighter.query.filter_by(name="Nika Beroshvili").first()
            gigi = Fighter.query.filter_by(name="Gigi Kenkishvili").first()
            if nika_b and gigi:
                fight = Fight(
                    fighter1=nika_b,
                    fighter2=gigi,
                    event=event,
                    weight_class="Middleweight"
                )
                db.session.add(fight)

            sandro_d = Fighter.query.filter_by(name="Sandro Datiashvili").first()
            nika_a = Fighter.query.filter_by(name="Nika Antadze").first()
            if sandro_d and nika_a:
                fight = Fight(
                    fighter1=sandro_d,
                    fighter2=nika_a,
                    event=event,
                    weight_class="Middleweight"
                )
                db.session.add(fight)

        db.session.commit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)