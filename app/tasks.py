# from time import sleep
import requests
from app import db
from app.models import Batting, Bowling, Fielding
from bs4 import BeautifulSoup
import re
import json
from app import socketio
from threading import Lock

# Keeps track of all upcoming, live and recently concluded matches.
matches = [] # Ideally should be in database. But this is okay bcoz number of matches is quite less (< 10)
matches_lock = Lock()

def get_matches_as_raw_data():
    """
    Returns a dictionary with all live
    and upcoming match details
    """
    URL = 'https://www.espncricinfo.com/'

    # Get HTML page and `soup` it
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html5lib')

    # Scrap details of matches from HTML page
    result = re.findall('data: {.*}', soup.prettify())[0] # As of 28 Oct 2019, it works. This may not work if espn updates their website
    data = json.loads(result[6:])

    return data

def get_matches_from_raw_data(data):
    """
    Extracts relevant details from data
    and returns live and upcoming matches.
    """
    s_matches = []
    for league in data['sports'][0]['leagues']:
        for event in league['events']:
            teams = []
            for t in event['competitors']:
                team = {}
                team['logo'] = t['logo']
                team['name'] = t['name']
                team['score'] = t['score']
                team['winner'] = t['winner']
                teams.append(team)
            match = {}
            match['status'] = event['fullStatus']['type']['description']
            match['link'] = event['link'] 
            match['id'] = event['id']
            match['teams'] = teams
            s_matches.append(match)
    return s_matches

def emit_matches(socketio, matches_data):
    """
    `Emits` back details of matches via socketio.
    If the client requests it, reply goes back 
    to the client.
    If the server requests it, reply will be broadcasted
    to all clients.
    **IMPORTANT**: This also updates the `matches` global variable.
    """
    global matches
    matches = get_matches_from_raw_data(matches_data)
    socketio.emit('matches', {'matches': matches})

def update_matches(period=0, infinite=True):
    """
    Broadcasts updates in latest matches to all clients.
    
    `period`: Keeps checking for updates at `period` seconds intervals
    `infinite`: If True, then this function runs forever, else will `emit`
                latest match details.
    """
    matches_data = {}
    while infinite:
        temp_data = get_matches_as_raw_data()
        with matches_lock:
            if temp_data != matches_data:
                matches_data = temp_data
                emit_matches(socketio, matches_data)
        socketio.sleep(period)

def get_match_from_id(match_id):
    """
    Returns match from `matches` array 
    based on `match_id`.
    If `match_id` doesn't match any of the 
    matches in `matches`, `None` is returned.
    """
    for match in matches:
        if match_id == match['id']:
            return match
    return None
        

def get_match_raw_data(match_id):
    """
    Gets match data from `URL` of the match in 
    cricinfo.
    """
    # Get match URL
    global matches
    match = get_match_from_id(match_id)
    URL = match['link']

    # Get HTML page and `soup` it
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    # Scrap match data from HTML page
    result = re.findall('window.__INITIAL_STATE__ = {.*}', soup.prettify())[0]
    temp_data = json.loads(result[27:])

    # Extract data from REST API URL in `data`
    apiURL = temp_data['apiUrls']['urls'][0]
    data = requests.get(apiURL).json()
    # print(json.dumps(data))
    return data

# Team details include: Players playing in both teams, TODO: score of each player

def get_team_details(match_id):
    """
    Returns a dictionary with given team details.
    `match_id`: Index in matches global variable
    """
    data = get_match_raw_data(match_id)
    team_details = get_team_details_from_raw_data(data)
    return team_details

def get_team_details_from_raw_data(data):
    """
    Extracts relevant details from data 
    and returns team details.
    """
    match = {}

    #TODO: JSON

    # Get roster
    teams = []
    for roster in data['rosters']:
        team = []
        for p in roster['roster']:
            player = {}
            player['name'] = p['athlete']['battingName']
            player['id'] = get_player_id_from_name(player['name'])
            player['score'] =  get_player_score_from_id(player['id'])
            team.append(player)
        teams.append(team)
    
    match['teams'] = teams
    return match

# Match details include: live score, all player detalis (runs scored, wickets taken, etc)

def get_match_details(match_id):
    """
    Returns a dictionary with given match details.
    `match_id`: Index in matches global variable
    """
    data = get_match_raw_data(match_id)
    match_details = get_match_details_from_raw_data(data)
    return match_details

def get_match_details_from_raw_data(data):
    """
    Extracts relevant details from data
    and returns match details.
    """
    match = {}
    scores = []
    for roster in data['rosters']:
        s = []
        for player in roster['roster']:
            id = get_player_id_from_name(player['athlete']['battingName'])
            score = get_player_score_from_id(id)
            # TODO: Define logic for new score
            new_score = score
            s.append(new_score)
        scores.append(s)
    match['matchcards'] = data['matchcards']
    match['scores'] = scores
    return match

def update_match_details(match_id, period):
    """
    Sends match details clients who ask for it.
    
    `period`: Keeps checking for updates at `period` seconds intervals
    """
    while True:
        with matches_lock:
            match = get_match_from_id(match_id)
            match_details = get_match_details(match_id)
            emit_match_details(match_details)            
        socketio.sleep(period)

def emit_match_details(match_details):
    """
    `Emits` back match details via socketio.
    If the client requests it, reply goes back 
    to the client.
    If the server requests it, reply will be broadcasted
    to all clients.
    """
    print('send back live match')
    socketio.emit('live_match', {'match': match_details})

def cache_match_data():
    """
    To speed up fetching match data.
    """
    pass

def get_player_id_from_name(player_name):
    """
    Get player from `Fielding` table.
    If not present, then is added to `Fielding` table 
    with default low score and new id is returned
    """
    search="%{}%".format(player_name)
    player = Fielding.query.filter(Fielding.player.like(search)).first()
    if player is None:
        new_player = Fielding(player=player_name)
        new_player.score = 0
        db.session.add(new_player)
        db.session.commit()
        return new_player.id
    return player.id

def get_player_score_from_id(player_id):
    """
    Get score of player from batting
    """
    return db.session.query(Fielding).get(player_id).score
    #TODO: Implement this correctly
    score = 0
    player_name = db.session.query(Fielding).get(player_id)
    score1 = db.session.query(Batting).filter_by(player=player_name)
    score2 = db.session.query(Bowling).filter_by(player=player_name).first()
    score3 = db.session.query(Fielding).filter_by(player=player_name).first()
    if score1 is not None:
        score += score1
    if score2 is not None:
        score += score2
    if score3 is not None:
        score += score3
    return score/3