#!/usr/bin/env python3

import time
from operator import itemgetter


class EventHandler:
    def __init__(self, event_list):
        self.event_list = event_list

    def add_event(self, event):
        category, person = self.parse_event(event)
        event_time = self.get_time()
        event = {
            'id': len(self.event_list) + 1,
            'category': category,
            'person': person,
            'text': event,
            'time': event_time
        }
        self.event_list.append(event)
        self.event_list = self.sort_events_by_time(self.event_list)
        return event

    def get_all_event(self):
        return self.event_list

    def get_events(self, field=None, value=None, count=10):
        selected_events = []
        if not field:
            return self.event_list[0:count]
        elif field == 'time':
            value = int(value)
            for event in self.event_list:
                if event[field] < value:
                    selected_events.append(event)
                if len(selected_events) == count:
                    break
        else:
            for event in self.event_list:
                if event[field] == value:
                    selected_events.append(event)
                if len(selected_events) == count:
                    break
        return selected_events

    def get_last_ten(self):
        return self.get_events()

    def get_last(self, count):
        return self.get_events(count=count)

    def get_last_by_field(self, field, value):
        return self.get_events(field, value)

    def get_event_by_id(self, event_id):
        return next(
            (event for event in self.event_list if event['id'] == event_id),
            None)

    @staticmethod
    def parse_event(event):
        """We like to make a great programs #update @all"""
        words = event.split()

        # defaults
        person = 'all'
        category = 'update'
        for word in words:
            if word.startswith('#'):
                category = word.strip('#')
            elif word.startswith('@'):
                person = word.strip('@')
        return category, person

    @staticmethod
    def get_time():
        return int(time.time())

    @staticmethod
    def sort_events_by_time(event_list):
        return sorted(
            event_list, key=itemgetter('time'), reverse=True)
