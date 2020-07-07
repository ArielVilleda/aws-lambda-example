from os import environ
from aws_lambda_cors.utils.response import AwsLambdaResponse

ALLOWED_ORIGINS = environ["ALLOWED_ORIGINS"]
DEFAULT_HEADERS = {
    "Access-Control-Allow-Origin": ALLOWED_ORIGINS,
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,HEAD"
}


def basic(body, headers=None, status_code=200):
    headers_ = headers if headers is not None else DEFAULT_HEADERS
    return AwsLambdaResponse(body=body, headers=headers_, status_code=status_code)

def unprocessable_entity(validation_errors:list):
    errors = {
        "errors": validation_errors
    }
    return basic(body=errors, status_code=422)

def email_send_error():
    errors = {
        "errors": [
            {'email' : 'the email was not sent'}
        ]
    }
    return basic(body=errors, status_code=422)