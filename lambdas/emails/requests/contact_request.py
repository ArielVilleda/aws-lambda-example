from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
import json

class RequestInputs(Inputs):
    _SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema",
        "type": "object",
        "required": [
            "email", "name", "phone", "message"
        ],
        "properties": {
            "email": {
                "type": "string",
                "format": "email"
            },
            "name": {
                "type": "string",
                "minLength": 2,
                "maxLength": 32
            },
            "phone": {
                "type": "string",
                "minLength": 8,
                "maxLength": 32
            },
            "message": {
                "type": "string",
                "minLength": 16,
                "maxLength": 64
            }
        }
    }
    json = [JsonSchema(schema=_SCHEMA)]


class ContactRequest(object):
    def __init__(self, body):
        self.body = body
        self.json = json.loads(body)

    def validate(self):
        inputs = RequestInputs(self)
        if inputs.validate():
            return None
        else:
            return inputs.errors