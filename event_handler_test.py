#!/usr/bin/env python3

import unittest

from event_handler import EventHandler
from sample_events import sample_events


class EventHandlerTestCase(unittest.TestCase):

    def __init__(self, method):
        unittest.TestCase.__init__(self, method)
        self.not_default_event = 'Hey its a tweet from Me #update @all'
        self.default_event = 'Hey its a default event without stuff'

    def setUp(self):
        event_list = []
        self.event_service = EventHandler(event_list)
        self.sample_events = self.event_service.sort_events_by_time(sample_events)

    def test_add_event_with_defaults(self):
        result = self.event_service.add_event(self.default_event)

        since_epoch = self.event_service.get_time()

        expected = {
            'id': 1,
            'category': 'update',
            'person': 'all',
            'text': self.default_event,
            'time': since_epoch
        }
        self.assertDictEqual(result, expected)

    def test_add_event_no_defaults(self):
        result = self.event_service.add_event(self.not_default_event)

        since_epoch = self.event_service.get_time()

        expected = {
            'id': 1,
            'category': 'update',
            'person': 'all',
            'text': self.not_default_event,
            'time': since_epoch
        }
        self.assertDictEqual(result, expected)

    def test_add_event_adds_to_event_list(self):
        result = self.event_service.add_event(self.not_default_event)
        self.assertListEqual(self.event_service.event_list, [result])

    def test_append_to_not_empty_event_list(self):
        event1 = self.event_service.add_event(self.not_default_event)
        event2 = self.event_service.add_event(self.default_event)
        self.assertListEqual(self.event_service.event_list, [event1, event2])

    def test_add_nine_get_nine(self):
        self.event_service.event_list = self.sample_events[0:9]
        result = self.event_service.get_last_ten()
        self.assertEqual(len(result), 9)
        self.assertListEqual(result, self.sample_events[0:9])

    def test_add_ten_get_ten(self):
        self.event_service.event_list = self.sample_events[0:10]
        result = self.event_service.get_last_ten()
        self.assertEqual(len(result), 10)
        self.assertListEqual(result, self.sample_events[0:10])

    def test_add_eleven_get_ten(self):
        self.event_service.event_list = self.sample_events[0:11]
        result = self.event_service.get_last_ten()
        self.assertEqual(len(result), 10)
        self.assertListEqual(result, self.sample_events[0:10])

    def test_add_eleven_get_eleven(self):
        self.event_service.event_list = self.sample_events[0:11]
        result = self.event_service.get_last(11)
        self.assertEqual(len(result), 11)
        self.assertListEqual(result, self.sample_events[0:11])

    def test_get_last_by_field(self):
        self.event_service.event_list = self.sample_events[0:10]
        result = self.event_service.get_last_by_field('category', 'poll')
        self.assertListEqual(result, [self.sample_events[0],
                                      self.sample_events[4],
                                      self.sample_events[5]])

    def test_get_last_by_field_bewlo_ten(self):
        self.event_service.event_list = self.sample_events
        result = self.event_service.get_last_by_field('category', 'update')
        expected = [self.sample_events[1], self.sample_events[2],
                    self.sample_events[6], self.sample_events[9],
                    self.sample_events[10]]
        self.assertEqual(len(result), 5)
        self.assertListEqual(result, expected)

    def test_get_last_by_field_above_ten(self):
        self.event_service.event_list = self.sample_events
        [self.event_service.add_event(self.not_default_event) for _ in range(6)]
        result = self.event_service.get_last_by_field('category', 'update')
        expected = self.event_service.event_list[0:6] + \
            [self.sample_events[1], self.sample_events[2],
                self.sample_events[6], self.sample_events[9]]
        self.assertEqual(len(result), 10)
        self.assertListEqual(result, expected)

    def test_get_by_id(self):
        self.event_service.event_list = self.sample_events
        result = [self.event_service.get_event_by_id(11)]
        expected = [self.sample_events[0]]
        self.assertEqual(len(result), 1)
        self.assertListEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
