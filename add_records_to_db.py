import pandas as pd
from app import db
from app.models import Batting, Bowling, Fielding

# Batting
df = pd.read_csv('csv/batting.csv')

# Get a better scoring system

for index, row in df.iterrows():
    p = Batting(player=row['Player'])
    p.span = row['Span']
    p.matches = row['Mat']
    p.innings = row['Inns']
    p.no = row['NO']
    p.runs = row['Runs']
    p.hs = row['HS']
    p.ave = row['Ave']
    p.bf = row['BF']
    p.sr = row['SR']
    p.hundreds = row['100']
    p.fifties = row['50']
    p.ducks = row['0']
    p.score = 100
    db.session.add(p)

db.session.commit()
print('Added Batsman records')

# Bowling
df = pd.read_csv('csv/bowling.csv')

for index, row in df.iterrows():
    p = Bowling(player=row['Player'])
    p.span = row['Span']
    p.matches = row['Mat']
    p.innings = row['Inns']
    p.balls = row['Balls']
    p.runs = row['Runs']
    p.wickets = row['Wkts']
    p.best = row['BBI']
    p.ave = row['Ave']
    p.econ = row['Econ']
    p.sr = row['SR']
    p.four = row['4']
    p.fivee = row['5']
    p.score = 100
    db.session.add(p)

db.session.commit()
print('Added Bowling records')

# Fielding
df = pd.read_csv('csv/fielding.csv')

for index, row in df.iterrows():
    p = Fielding(player=row['Player'])
    p.span = row['Span']
    p.matches = row['Mat']
    p.innings = row['Inns']
    p.dismissals = row['Dis']
    p.catches = row['Ct']
    p.stumpings = row['St']
    p.catch_wk = row['Ct Wk']
    p.catch_fi = row['Ct Fi']
    p.best = row['MD']
    p.score = 100
    db.session.add(p)

db.session.commit()
print('Added Fielding records')