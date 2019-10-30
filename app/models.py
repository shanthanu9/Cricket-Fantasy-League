from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

# UserMixin provides generic implementations of 
# is_authenticated, is_active, is_anonymous and 
# get_id(), all of which are required for flask
# -login liibrary.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    score = db.Column(db.Integer)
    match_id = db.Column(db.String(20))

    chosen_players = db.relationship('ChosenPlayer')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # TODO: Randomly assign a profile pic to each user...

class Batting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(64))
    span = db.Column(db.String(10))
    matches = db.Column(db.String(6))
    innings = db.Column(db.String(6))
    no = db.Column(db.String(6))
    runs = db.Column(db.String(6))
    hs = db.Column(db.String(6))
    ave = db.Column(db.String(6))
    bf = db.Column(db.String(6))
    sr = db.Column(db.String(6))
    hundreds = db.Column(db.String(6))
    fifties = db.Column(db.String(6))
    ducks = db.Column(db.String(6))
    score = db.Column(db.Float)

class Bowling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(64))
    span = db.Column(db.String(10))
    matches = db.Column(db.String(6))
    innings = db.Column(db.String(6))
    balls = db.Column(db.String(6))
    runs = db.Column(db.String(6))
    wickets = db.Column(db.String(6))
    best = db.Column(db.String(6))
    ave = db.Column(db.String(6))
    econ = db.Column(db.String(6))
    sr = db.Column(db.String(6))
    four = db.Column(db.String(6))
    five = db.Column(db.String(6))
    score = db.Column(db.Float)

class Fielding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(64))
    span = db.Column(db.String(10))
    dismissals = db.Column(db.String(6))
    catches = db.Column(db.String(6))
    stumpings =db.Column(db.String(6))
    catch_wk = db.Column(db.String(6))
    catch_fi = db.Column(db.String(6))
    best = db.Column(db.String(20))
    score = db.Column(db.Float)

    users = db.relationship('ChosenPlayer')

class ChosenPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('fielding.id'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))