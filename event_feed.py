#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request

from event_handler import EventHandler

app = Flask(__name__)

event_list = []

event_service = EventHandler(event_list)


@app.route('/feeds/api/v1/events')
def get_last_ten():
    last_events = event_service.get_last_ten()
    if not last_events:
        abort(404)
    return jsonify({'events': last_events}), 200


@app.route('/feeds/api/v1/events/<string:field>/<string:value>')
def get_last_by_field(field, value):
    events_by_field = event_service.get_last_by_field(field, value)
    if not events_by_field:
        abort(404)
    return jsonify({'events': events_by_field}), 200


@app.route('/feeds/api/v1/event/<int:event_id>', methods=['GET'])
def get_last_by_id(event_id):
    events_by_id = event_service.get_event_by_id(int(event_id))
    if not events_by_id:
        abort(404)
    return jsonify({'event': events_by_id}), 200


@app.route('/feeds/api/v1/event', methods=['POST'])
def add_event():
    if not request.data:
        abort(400)
    event = event_service.add_event(request.data.decode("utf-8"))
    return jsonify({'event': event}), 201


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify(
        {'error': 'Invalid request, no event found in the request body!'}))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No events found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
