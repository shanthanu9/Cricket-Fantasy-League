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
    # Give some default value to score
    score = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # TODO: Randomly assign a profile pic to each user...

@login.user_loader
def load_user(id):
    return User.query.get(int(id))