from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data
events = []
next_id = 1

class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

# Seed initial events
events.append(Event(1, "Tech Meetup"))
events.append(Event(2, "Python Workshop"))

@app.route('/events', methods=['POST'])
def create_event():
    global next_id
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Missing title"}), 400
    new_event = Event(next_id, data['title'])
    events.append(new_event)
    next_id += 1
    return jsonify({"id": new_event.id, "title": new_event.title}), 201

@app.route('/events/<int:id>', methods=['PATCH'])
def update_event(id):
    data = request.get_json()
    event = next((e for e in events if e.id == id), None)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    if 'title' in data:
        event.title = data['title']
    return jsonify({"id": event.id, "title": event.title}), 200

@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    global events
    event = next((e for e in events if e.id == id), None)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    events = [e for e in events if e.id != id]
    return '', 204

if __name__ == '__main__':
    app.run(port=5555)