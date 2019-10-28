# from time import sleep
import requests
from bs4 import BeautifulSoup
import re
import json
from app import socketio
from pprint import pprint
import sys

# Keeps track of all upcoming, live and recently concluded matches.
matches = [] # Ideally should be in database. But this is okay bcoz number of matches is quite less (< 10)

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
    Broadcasts updates in match details to all clients.
    
    `period`: Keeps checking for updates at `period` seconds intervals
    `infinite`: If True, then this function runs forever, else will `emit`
                latest match details.
    """
    matches_data = {}
    while infinite:
        temp_data = get_matches_as_raw_data()
        if temp_data != matches_data:
            matches_data = temp_data
            emit_matches(socketio, matches_data)
            cache_match_details()
        socketio.sleep(period)

def get_match_details(match_id):
    """
    Returns a dictionary with given match details.
    `match_id`: Index in matches global variable
    """
    # Get match URL
    global matches
    match = matches[match_id]
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

    print('SIZE: ' + str(sys.getsizeof(data)))

    match_details = get_match_details_from_raw_data(data)
    return match_details

def get_match_details_from_raw_data(data):
    """
    Extracts relevant details from data 
    and returns match details.
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

def cache_match_details():
    """
    To speed up fetching match details.
    """
    pass