from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import json
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    predictions = db.relationship('Prediction', backref='user', lazy=True)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float)
    verdict = db.Column(db.String(100))
    advice = db.Column(db.Text)  # New
    category_scores = db.Column(db.JSON)  # New: store dictionary
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def get_category_scores(self):
        return json.loads(self.category_scores or "{}")
