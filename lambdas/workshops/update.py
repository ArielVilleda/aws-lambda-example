from pynamodb.exceptions import DoesNotExist

from models.workshop import Workshop
from requests.update_request import UpdateRequest
import response_structures

def handler(event, context):
    """
    Example:
        'url': /workshop/{workshopId}
        'type': PATCH
        'body':{
            "activity" : "Entrevistas a profundidad",
            "theme" : "Realizadas a actores clave",
            "place" : "Por Definir",
            "available" : 1,
            "schedule" : [
                {
                    "date" : "00/00/0000",
                    "init_time" : "10:00:00",
                    "end_time" : "13:00:00"
                },
                {
                    "date" : "06/08/2020",
                    "init_time" : "10:00:00",
                    "end_time" : "13:00:00"
                }
            ]
        }
    """

    try:
        workshop_id = event['pathParameters']['workshopId']
        workshop_item = Workshop.get(workshop_id)
    except DoesNotExist:
        return response_structures.workshop_not_found().parse()

    request = UpdateRequest(event['body'])
    
    validation_errors = request.validate()
    if validation_errors:
        return response_structures.unprocessable_entity(validation_errors).parse()

    workshop_item.update(**(request.json)).save()

    response_body = {
        'workshop': workshop_item.to_dictionary()
    }
    return response_structures.basic(body=response_body, status_code=200).parse()

