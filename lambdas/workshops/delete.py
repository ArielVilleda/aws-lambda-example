from pynamodb.exceptions import DoesNotExist

from models.workshop import Workshop
import response_structures


def handler(event, context):
    """
    Exmaple
    'url': /workshop/{workshopId}
    """
    try:
        workshop_id = event['pathParameters']['workshopId']
        workshop_item = Workshop.get(workshop_id)
    except DoesNotExist:
        return response_structures.workshop_not_found().parse()

    workshop_item.delete()

    response_body = {
        'workshop': workshop_item.to_dictionary()
    }
    return response_structures.basic(body=response_body, status_code=200).parse()