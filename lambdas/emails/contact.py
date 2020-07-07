from models.email_contact import EmailContact
from requests.contact_request import ContactRequest
import response_structures
from mailing.email_sender import send_contact_mail

def handler(event, context):
    """
    Example:
        'url': /email/contact
        'type': POST
        'body':{
            "email" : "ariel.mvilleda@gmail.com",
            "name" : "Ariel Villeda",
            "phone" : "20200606",
            "message" : "Todo Shiido, Man"
        }
    """

    request = ContactRequest(event['body'])
    
    validation_errors = request.validate()
    if validation_errors:
        return response_structures.unprocessable_entity(validation_errors).parse()

    email_contact_item = EmailContact.create(
        email=request.json['email'],
        name=request.json['name'],
        phone=request.json['phone'],
        message=request.json['message']
    )

    if not send_contact_mail(email_contact_item):
        return response_structures.email_send_error().parse()

    response_body = {
        'email_contact': email_contact_item.to_dictionary(attr_filter={'email', 'name', 'created_at', 'phone', 'message'})
    }
    return response_structures.basic(body=response_body, status_code=200).parse()

