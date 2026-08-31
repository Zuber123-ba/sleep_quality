from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class SleepHistory(db.Model):
    __tablename__ = "sleep_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    sleep_quality = db.Column(db.String(10), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
