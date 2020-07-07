from uuid import uuid4
from os import environ
from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, ListAttribute)

from .custom_attributes import ScheduleMap

ENV = environ['ENV']
TABLE_NAME = environ['WORKSHOP_TABLE']
AMAZON_REGION = environ['AMAZON_REGION']
DYNAMO_DB_LOCAL_URL = environ['DYNAMO_DB_LOCAL_URL']

class Workshop(Model):
    class Meta:
        table_name = TABLE_NAME
        region = AMAZON_REGION
        if ENV == 'local':
            host = DYNAMO_DB_LOCAL_URL

    id = UnicodeAttribute(hash_key=True)

    activity = UnicodeAttribute(null=False)
    theme = UnicodeAttribute(null=False, default="")
    schedule = ListAttribute(of=ScheduleMap, null=False)
    place = UnicodeAttribute(null=False)
    available = NumberAttribute(null=False, default=0)


    def to_dictionary(self, attr_filter:set={'id', 'activity', 'theme',
                    'schedule', 'place', 'available'}):
        result_dict = {}

        if 'id' in attr_filter: result_dict['id'] = self.id
        if 'activity' in attr_filter: result_dict['activity'] = self.activity
        if 'theme' in attr_filter: result_dict['theme'] = self.theme
        if 'place' in attr_filter: result_dict['place'] = self.place
        if 'available' in attr_filter: result_dict['available'] = self.available
        if 'schedule' in attr_filter: result_dict['schedule'] = self._schedule_parse()

        return result_dict

    def _schedule_parse(self):
        rlist = list()
        for item in self.schedule:
            rval = {}
            for key in item:
                rval[key] = item[key]
            rlist.append(rval)
        return rlist

    def update(self, activity, theme, place, available, schedule:list):
        self.activity = activity
        self.theme = theme
        self.place = place
        self.available = available
        self.schedule = schedule
        return self

    @staticmethod
    def create(activity, theme, place, available, schedule:list):
        item = Workshop()

        item.id = str(uuid4())
        item.activity = activity
        item.theme = theme
        item.place = place
        item.available = available
        item.schedule = schedule

        item.save()
        return item

    @staticmethod
    def list():
        query_items = [i for i in Workshop.scan()]  # Returns ALL items in Table
        return query_items
