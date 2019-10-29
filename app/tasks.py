# from time import sleep
import requests
from app import db
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
    return data['matchcards']

def update_match_details(match_id, period):
    """
    Broadcasts updates in match details to all clients.
    
    `period`: Keeps checking for updates at `period` seconds intervals
    """
    while True:
        with matches_lock:
            match = matches[match_id]
            match_details = get_match_details(match_id)
            emit_match_details(socketio, match_details)            
        socketio.sleep(period)

def emit_match_details(socketio, match_details):
    """
    `Emits` back match details via socketio.
    If the client requests it, reply goes back 
    to the client.
    If the server requests it, reply will be broadcasted
    to all clients.
    """
    socketio.emit('live-match', {'match': match_details})

def cache_match_data():
    """
    To speed up fetching match data.
    """
    pass


def get_player_score(player_name):
    """
    Give player score based on their record.
    Player not present in database will be 
    assigned a default low score.
    """
    low_score = 5
    high_score = 50
    pass


