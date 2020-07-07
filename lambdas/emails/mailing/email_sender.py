from os import environ
from botocore.exceptions import ClientError
import boto3


# This address must be verified with Amazon SES.
SENDER = "Contacto CEA <contacto@quesadillalab.mx>"
# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AMAZON_REGION = environ['AMAZON_REGION']
# The character encoding for the email.
CHARSET = "UTF-8"


def send_contact_mail(contact_item:object):
    email_body = {}
    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    email_body['recipient_list'] = ["ariel@quesadillalab.mx"]
    # The subject line for the email.
    email_body['subject'] = "Conjunto Estadio Azteca | Contacto"

    # The email body for recipients with non-HTML email clients.
    email_body['body_text'] = """
    Nombre: {0}, \r\n
    Correo: {1}, \r\n
    Teléfono: {2}, \r\n
    Fecha: {3}, \r\n
    Mesaje: {4}
    """.format(contact_item.name, contact_item.email, contact_item.phone, 
                contact_item.created_at, contact_item.message)

    # The HTML body of the email.
    email_body['body_html'] = """<html>
    <head></head>
    <body>
        <h1>CONTACTO CONJUNTO ESTADIO AZTECA</h1>
        <ul>
        <li>Nombre: {0}</li>
        <li>Correo: {1}</li>
        <li>Teléfono: {2}</li>
        <li>Fecha: {3}</li>
        <li>Mesaje: {4}</li>
        <ul>
    </body>
    </html>
    """.format(contact_item.name, contact_item.email, contact_item.phone, 
                contact_item.created_at, contact_item.message)
    if not _sender(email_body):
        return False
    return True


def _sender(email:dict):
    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AMAZON_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': email['recipient_list'],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': email['body_html'],
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': email['body_text'],
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': email['subject'],
                },
            },
            Source=SENDER
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
    else:
        # print(response['MessageId'])
        return response