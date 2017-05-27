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
    return jsonify({'events': last_events})


@app.route('/feeds/api/v1/events/<string:field>/<string:value>')
def get_last_by_field(field, value):
    events_by_field = event_service.get_last_by_field(field, value)
    if not events_by_field:
        abort(404)
    return jsonify({'events': events_by_field})


@app.route('/feeds/api/v1/events/<int:id>')
def get_last_by_field(field, value):
    events_by_field = event_service.get_last_by_field(field, value)
    if not events_by_field:
        return 'No events found!'
    return jsonify({'events': events_by_field})


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)