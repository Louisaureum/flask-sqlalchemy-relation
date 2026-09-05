# server/app.py
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Helper to format speaker with optional bio
def speaker_to_dict(speaker):
    bio_text = speaker.bio.bio_text if speaker.bio else "No bio available"
    return {
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": bio_text
    }

@app.route('/')
def index():
    return '<h1>EventWise API</h1>'

# Event Endpoints
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = [{"id": e.id, "name": e.name, "location": e.location} for e in events]
    return make_response(jsonify(events_list), 200)

@app.route('/events/<int:id>/sessions', methods=['GET'])
def get_event_sessions(id):
    event = Event.query.get(id)
    if not event:
        return make_response(jsonify({"error": "Event not found"}), 404)
    sessions = event.sessions
    sessions_list = [
        {"id": s.id, "title": s.title, "start_time": s.start_time.isoformat()}
        for s in sessions
    ]
    return make_response(jsonify(sessions_list), 200)

# Speaker Endpoints
@app.route('/speakers', methods=['GET'])
def get_speakers():
    speakers = Speaker.query.all()
    speakers_list = [{"id": s.id, "name": s.name} for s in speakers]
    return make_response(jsonify(speakers_list), 200)

@app.route('/speakers/<int:id>', methods=['GET'])
def get_speaker(id):
    speaker = Speaker.query.get(id)
    if not speaker:
        return make_response(jsonify({"error": "Speaker not found"}), 404)
    return make_response(jsonify(speaker_to_dict(speaker)), 200)

# Session Endpoints
@app.route('/sessions/<int:id>/speakers', methods=['GET'])
def get_session_speakers(id):
    session = Session.query.get(id)
    if not session:
        return make_response(jsonify({"error": "Session not found"}), 404)
    speakers = session.speakers
    speakers_list = [speaker_to_dict(s) for s in speakers]
    return make_response(jsonify(speakers_list), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)