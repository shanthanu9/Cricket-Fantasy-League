from app import socketio
from threading import Lock
from app.tasks import update_matches, get_matches, emit_matches
from flask_socketio import SocketIO, emit

# For backgound processes
thread = None
thread_lock = Lock()

@socketio.on('connect')
def connect():
    # Update connected user with latest match details
    matches_data = get_matches()
    emit_matches(socketio, matches_data)
    print('User connected')
    global thread
    with thread_lock:
        if thread is None:
            period = 10 # 10 s
            thread = socketio.start_background_task(update_matches, period)