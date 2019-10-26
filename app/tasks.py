# from time import sleep
import requests
from bs4 import BeautifulSoup
import re
import json
from rq import get_current_job
from app import socketio
from pprint import pprint

def get_matches():
    """
    Returns a dictionary with all live
    and upcoming match details
    """
    job = get_current_job()
    URL = 'https://www.espncricinfo.com/'

    # Get HTML page and `soup` it
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html5lib')

    # Scrap match data from HTML page
    result = re.findall('data: {.*}', soup.prettify())[0] # As of 25 Oct 2019, it works. This may not work if espn updates their website
    data = json.loads(result[6:])

    return data

def get_matches_from_raw_data(data):
    """
    Helper function for update_matches.
    Extracts relevant details from data
    and returns live and upcoming matches.
    """
    s_leagues = []
    s_matches = []
    for league in data['sports'][0]['leagues']:
        s_leagues.append(league['abbreviation'])
        for event in league['events']:
            s_matches.append(event['description'])
    return (s_leagues, s_matches)

def emit_matches(socketio, matches_data):
    (s_leagues, s_matches) = get_matches_from_raw_data(matches_data)
    socketio.emit('matches', {
        'leagues': s_leagues,
        'matches': s_matches
    })

def update_matches(period=0, infinite=True):
    """
    Broadcasts updates in match details to all clients.
    
    `period`: Keeps checking for updates at `period` seconds intervals
    `infinite`: If True, then this function runs forever, else will `emit`
                latest match details.
    """
    matches_data = {}
    while infinite:
        temp_data = get_matches()
        if temp_data != matches_data:
            matches_data = temp_data
            emit_matches(socketio, matches_data)
        socketio.sleep(period)

def get_match_data(match_id):
    job = get_current_job()
    # URL for Cricket API
    url = 'https://cricscore-api.appspot.com/csa?id='+str(match_id)
    last_modified='Sun, 30 Jun 2000 23:58:22 IST'
    for i in range(10):
        response = requests.get(url, headers={'If-Modified-Since':last_modified})
        match = {}
        if response.status_code == 200:
            match = response.json()
            job.meta['match'] = match
            job.save_meta()
            last_modified = response.headers['Last-Modified']
            print('Got new data!')
        elif response.status_code == 304:
            print('Old data!')
            pass
        # Query every 10 seconds
        time.sleep(1)