from flask import request
from flask_login import current_user
from app import socketio
from threading import Lock
from app.tasks import update_matches, get_matches_as_raw_data, emit_matches, matches, update_match_details, get_team_details
from flask_socketio import SocketIO, emit
from app.models import User

# For backgound processes
matches_thread = None
live_match_thread = None
thread_lock = Lock()

@socketio.on('connect')
def connect():
    # Update connected user with latest matches
    matches_data = get_matches_as_raw_data()
    emit_matches(socketio, matches_data)
    print('User connected')
    global matches_thread, live_match_thread
    with thread_lock:
        if matches_thread is None:
            period = 3600 # 3600s
            matches_thread = socketio.start_background_task(update_matches, period)
        # if match_id is not None:
        #     period = 10 # 10s
        #     live_match_thread = socketio.start_background_task(update_match_details, socketio, match_id, period)
    
    user = User.query.filter_by(username=current_user.username).first()
    if user is not None and user.match_id is not None:
        period = 20 # 20s
        socketio.start_background_task(update_match_details, socketio, user.match_id, period)

@socketio.on('get_match')
def connect_team(msg):
    print('YEAH!!!!!!!!!!!!!!')
    match_id = msg['data']
    match = get_team_details(match_id)
    socketio.emit('match', {'match': match}, broadcast=False)
    print('Emitted team details')