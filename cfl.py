from app import app, socketio
from app.models import db, User
from app.tasks import get_matches, update_matches

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User,
        'get_matches': get_matches,
        'update_matches': update_matches
    }

if __name__ == '__main__':
    socketio.run(app)