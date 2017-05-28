#!/usr/bin/env python3

import unittest
import json

import event_feed
from sample_events import sample_events


class EventFeedTestCaseNotEmpty(unittest.TestCase):
    def __init__(self, method):
        unittest.TestCase.__init__(self, method)
        self.sample_events = sample_events
        self.default_event = 'Hey its a default event without stuff'

    def setUp(self):
        self.two_zero_zero = '200 OK'
        event_feed.event_service.event_list = self.sample_events
        self.app = event_feed.app.test_client()
        self.event_service = event_feed.event_service

    def test_get_last_ten(self):
        result = self.app.get('/feeds/api/v1/events')
        expected = self.sample_events[0:10]
        self.assertEqual(result.status, self.two_zero_zero)
        self.assertEqual(json.loads(result.data), {'events': expected})

    def test_get_last_by_field(self):
        result = self.app.get('/feeds/api/v1/events/person/all-friends')
        expected = [self.sample_events[0], self.sample_events[1],
                    self.sample_events[5], self.sample_events[10]]

        response_body = json.loads(result.data)
        self.assertEqual(result.status, self.two_zero_zero)
        self.assertEqual(len(response_body['events']), 4)
        self.assertEqual(response_body, {'events': expected})

    def test_get_by_id(self):
        result = self.app.get('/feeds/api/v1/event/5')
        expected = self.sample_events[6]

        response_body = json.loads(result.data)
        self.assertEqual(result.status, self.two_zero_zero)
        self.assertEqual(len(response_body), 1)
        self.assertEqual(response_body, {'event': expected})

    def test_get_by_time(self):
        result = self.app.get('/feeds/api/v1/events/time/1421604141')
        expected = {'events': self.sample_events[2:]}

        response_body = json.loads(result.data)
        self.assertEqual(result.status, self.two_zero_zero)
        self.assertDictEqual(response_body, expected)

    @staticmethod
    def get_data_from_json(response):
        return json.loads(response.get_data(as_text=True))