from models.workshop import Workshop
import response_structures


def handler(event, context):
    """
    Example:
        'url': /workshop
        'type': GET
    """
    query = Workshop.list()
    workshops = [workshop.to_dictionary() for workshop in query]

    response_body = {
        'workshops' : workshops
    }
    status_code = 200 if len(response_body['workshops'])>0 else 404
    return response_structures.basic(body=response_body, status_code=status_code).parse()


