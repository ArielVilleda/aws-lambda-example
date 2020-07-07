from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
import json

class RequestInputs(Inputs):
    _SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema",
        "type": "object",
        "required": [
            "activity", "schedule", "place"
        ],
        "properties": {
            "activity": {
                "type": "string",
                "minLength": 1,
                "maxLength": 64
            },
            "theme": {
                "type": "string",
                "minLength": 1,
                "maxLength": 64
            },
            "schedule": {
                "type": "array",
                "minItems" : 1,
                "items" : {
                    "type": "object",
                    "required" : ["date", "init_time", "end_time"],
                    "properties": {
                        "date" : {
                            "type": "string",
                            "format": "date"
                        },
                        "init_time" : {
                            "type": "string",
                            "pattern": "^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$"
                        },
                        "end_time" : {
                            "type": "string",
                            "pattern": "^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$"
                        }
                    }
                }
            },
            "place": {
                "type": "string",
                "minLength": 1,
                "maxLength": 64
            },
            "available": {
                "type": "number",
                "minimum": 0,
                "maximum": 1024
            }
        }
    }
    json = [JsonSchema(schema=_SCHEMA)]


class UpdateRequest(object):
    def __init__(self, body):
        self.body = body
        self.json = json.loads(body)

    def validate(self):
        inputs = RequestInputs(self)
        if inputs.validate():
            return None
        else:
            return inputs.errors