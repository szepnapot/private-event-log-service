#!/usr/bin/env python3

import unittest
import json

import event_feed


class EventFeedTestCaseEmpty(unittest.TestCase):
    def __init__(self, method):
        unittest.TestCase.__init__(self, method)
        self.not_default_event = 'Hey its a tweet from Me #yolo @all-friends'
        self.default_event = 'Hey its a default event without stuff'

    def setUp(self):
        self.four_zero_four = 'No events found'
        event_feed.event_service.event_list = []
        self.app = event_feed.app.test_client()
        self.event_service = event_feed.event_service

    def test_get_last_ten(self):
        result = self.app.get('/feeds/api/v1/events')
        data = self.get_data_from_json(result)
        self.assertEqual(data['error'], self.four_zero_four)
        self.assertEqual(result.status, '404 NOT FOUND')

    def test_get_by_field(self):
        result = self.app.get('/feeds/api/v1/category/update')
        data = self.get_data_from_json(result)
        self.assertEqual(data['error'], self.four_zero_four)
        self.assertEqual(result.status, '404 NOT FOUND')

    def test_get_last_by_id(self):
        result = self.app.get('/feeds/api/v1/event/1')
        data = self.get_data_from_json(result)
        self.assertEqual(data['error'], self.four_zero_four)
        self.assertEqual(result.status, '404 NOT FOUND')

    def test_add_event(self):
        result = self.app.post('/feeds/api/v1/event',
                               data=self.default_event)
        since_epoch = self.event_service.get_time()
        expected = {
            'id': 1,
            'text': 'Hey its a default event without stuff',
            'category': 'update',
            'person': 'all',
            'time': since_epoch
        }
        self.assertEqual(result.status, '201 CREATED')
        self.assertEqual(json.loads(result.data), {'event': expected})

    def test_add_full_event(self):
        result = self.app.post('/feeds/api/v1/event',
                               data=self.not_default_event)
        since_epoch = self.event_service.get_time()
        expected = {
            'id': 1,
            'text': 'Hey its a tweet from Me #yolo @all-friends',
            'category': 'yolo',
            'person': 'all-friends',
            'time': since_epoch
        }
        self.assertEqual(result.status, '201 CREATED')
        self.assertEqual(json.loads(result.data), {'event': expected})

    @staticmethod
    def get_data_from_json(response):
        return json.loads(response.get_data(as_text=True))