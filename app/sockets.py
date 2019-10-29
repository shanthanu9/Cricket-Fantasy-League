from app import socketio
from threading import Lock
from app.tasks import update_matches, get_matches_as_raw_data, emit_matches, matches, update_match_details
from flask_socketio import SocketIO, emit

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
            period = 10 # 10s
            matches_thread = socketio.start_background_task(update_matches, period)
        # if match_id is not None:
        #     period = 10 # 10s
        #     live_match_thread = socketio.start_background_task(update_match_details, period, match_id)

# @socketio.on('')