# server/models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Optional: naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

# Association table for many-to-many between sessions and speakers
session_speakers = db.Table(
    'session_speakers',
    metadata,
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('speaker_id', db.Integer, db.ForeignKey('speakers.id'), primary_key=True)
)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)

    # One-to-Many: Event has many Sessions
    sessions = db.relationship('Session', back_populates='event', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Event {self.name}, Location: {self.location}>'

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    start_time = db.Column(db.DateTime)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    event = db.relationship('Event', back_populates='sessions')
    # Many-to-Many with Speaker
    speakers = db.relationship('Speaker', secondary=session_speakers, back_populates='sessions')

    def __repr__(self):
        return f'<Session {self.title}, Start: {self.start_time}>'

class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # One-to-One with Bio
    bio = db.relationship('Bio', back_populates='speaker', uselist=False, cascade='all, delete-orphan')

    # Many-to-Many with Session
    sessions = db.relationship('Session', secondary=session_speakers, back_populates='speakers')

    def __repr__(self):
        return f'<Speaker {self.name}>'

class Bio(db.Model):
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.String)

    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'))

    speaker = db.relationship('Speaker', back_populates='bio')

    def __repr__(self):
        return f'<Bio for Speaker {self.speaker_id}: {self.bio_text[:20]}...>'