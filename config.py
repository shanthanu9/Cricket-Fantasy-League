import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Assumes you have a user named 'shanthanu' with password 'shanthanu' in your database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://shanthanu:shanthanu@localhost/cfl'
    #TODO: May have to change this for leaderboard
    SQLALCHEMY_TRACK_MODIFICATIONS = False