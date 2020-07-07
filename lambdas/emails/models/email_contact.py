from uuid import uuid4
from os import environ
from pynamodb.models import Model
from pynamodb.indexes import (GlobalSecondaryIndex, AllProjection)
from pynamodb.attributes import UnicodeAttribute
import datetime as dt
import pytz # to use as created_at date generator


ENV = environ['ENV']
TABLE_NAME = environ['EMAIL_CONTACT_TABLE']
AMAZON_REGION = environ['AMAZON_REGION']
DYNAMO_DB_LOCAL_URL = environ['DYNAMO_DB_LOCAL_URL']
ITEM_TIMEZONE = environ['TIME_ZONE']
EMAIL_CONTACT_CREATED_AT_INDEX = 'email_contact_created_at_index'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class CreatedAtIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = EMAIL_CONTACT_CREATED_AT_INDEX
        projection = AllProjection()
        read_capacity_units = 1
        write_capacity_units = 1

    created_at = UnicodeAttribute(hash_key=True)


class EmailContact(Model):
    class Meta:
        table_name = TABLE_NAME
        region = AMAZON_REGION
        if ENV == 'local':
            host = DYNAMO_DB_LOCAL_URL

    id = UnicodeAttribute(hash_key=True)

    created_at_index = CreatedAtIndex()
    created_at = UnicodeAttribute()

    email = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=False)
    phone = UnicodeAttribute(null=False)
    message = UnicodeAttribute(null=False)


    def to_dictionary(self, attr_filter:set={'id', 'email', 'name', 'created_at',
                    'phone', 'message'}):
        result_dict = {}
        for key in self.attribute_values:
            if key in attr_filter:
                result_dict[key] = self.__getattribute__(key)
        return result_dict

    @staticmethod
    def create(email, name, phone, message):
        
        item = EmailContact()
        
        item.id = str(uuid4())
        item.created_at = dt.datetime.now(pytz.timezone(ITEM_TIMEZONE)).strftime(DATE_FORMAT)
        item.email = email
        item.name = name
        item.phone = phone
        item.message = message
        
        item.save()
        return item
