import json
import hmac
import hashlib
import requests
import boto3
from jwt import decode


def lambda_handler(event, context):
    secret_values = get_secrets(['DEVOPS_EVENTS_SECRET_TOKEN', 'API_DEVOPS_EVENT_CATCHER'])
    secret_token = secret_values['DEVOPS_EVENTS_SECRET_TOKEN']
    api_devops_event_catcher = secret_values['API_DEVOPS_EVENT_CATCHER']

    if not is_signature_valid(event, secret_token):
        return response_forbidden()

    if not send_event_to_catcher(api_devops_event_catcher, secret_token):
        return response_internal_server_error()

    return response_success()

def get_secrets(secret_keys):
    secrets_client = boto3.client('secretsmanager')
    secret = secrets_client.get_secret_value(SecretId='DevOpsSecretStore')['SecretString']
    return {key: json.loads(secret)[key] for key in secret_keys}

def is_signature_valid(event, secret_token):
    headers = event.get('headers', {})
    body = event.get('body', '')
    signature = headers.get('X-Webhook-Signature')

    if not signature:
        return False

    try:
        options = {'iss': 'netlify', 'verify_iss': True, 'algorithm': 'HS256'}
        decoded = decode(signature, secret_token, options=options)
        return decoded.get('sha256') == hmac.new(secret_token.encode(), body.encode(), hashlib.sha256).hexdigest()
    except DecodeError:
        return False

def send_event_to_catcher(api_url, secret_token):
    record = {'Repo': 'thisisarchimedes/web', 'Event': 'deploy'}
    headers = {'X-Secret-Token': secret_token, 'Content-Type': 'application/json'}
    response = requests.post(api_url, json=record, headers=headers)
    return response.status_code == 200

def response_forbidden():
    return {'statusCode': 403, 'body': json.dumps('Forbidden')}

def response_internal_server_error():
    return {'statusCode': 500, 'body': json.dumps('Error sending data to API_DEVOPS_EVENT_CATCHER')}

def response_success():
    return {'statusCode': 200, 'body': json.dumps('Webhook processed successfully')}

