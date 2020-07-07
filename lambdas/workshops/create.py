from models.workshop import Workshop
from requests.create_request import CreateRequest
import response_structures

def handler(event, context):
    """
    Example:
        'url': /workshop
        'type': POST
        'body':{
            "activity" : "Módulo informativo",
            "theme" : "N/A",
            "schedule" : [
                {
                    "date" : "2020/06/01",
                    "init_time" : "10:00:00",
                    "end_time" : "18:00:00"
                },
                {
                    "date" : "2020/06/02",
                    "init_time" : "10:00:00",
                    "end_time" : "18:00:00"
                },
                {
                    "date" : "2020/06/03",
                    "init_time" : "10:00:00",
                    "end_time" : "18:00:00"
                },
                {
                    "date" : "2020/06/04",
                    "init_time" : "10:00:00",
                    "end_time" : "18:00:00"
                },
                {
                    "date" : "2020/06/05",
                    "init_time" : "10:00:00",
                    "end_time" : "18:00:00"
                },
                {
                    "date" : "2020/06/06",
                    "init_time" : "10:00:00",
                    "end_time" : "18:00:00"
                }
            ],
            "place" : "En Línea",
            "available" : 1
        }
    """

    request = CreateRequest(event['body'])
    
    validation_errors = request.validate()
    if validation_errors:
        return response_structures.unprocessable_entity(validation_errors).parse()

    workshop_item = Workshop.create(
        activity=request.json['activity'],
        theme=request.json['theme'],
        place=request.json['place'],
        available=request.json['available'],
        schedule=request.json['schedule']
    )

    response_body = {
        'workshop' : workshop_item.to_dictionary()
    }
    return response_structures.basic(body=response_body, status_code=200).parse()

