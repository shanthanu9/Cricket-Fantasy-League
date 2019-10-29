from app import app, socketio
from app.models import db, User
from app.tasks import get_matches_as_raw_data, update_matches
from flask_mail import Message
from app import mail

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User,
        'get_matches_as_raw_data': get_matches_as_raw_data,
        'update_matches': update_matches,
        'Message': Message,
        'mail': mail
    }

if __name__ == '__main__':
    # Cache match details before running the app
    socketio.run(app, debug=True)