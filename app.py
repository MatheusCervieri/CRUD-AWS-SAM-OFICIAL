import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Use LocalStack for local development
endpoint_url = 'http://localhost:4566'
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
table = dynamodb.Table('my-table')

def lambda_handler(event, context):
    operation = event['httpMethod']
    if operation == 'POST':
        return create(event)
    elif operation == 'GET':
        return read(event)
    elif operation == 'PUT':
        return update(event)
    elif operation == 'DELETE':
        return delete(event)
    else:
        return {
            'statusCode': 400,
            'body': 'Invalid operation'
        }

def create(event):
    data = json.loads(event['body'])
    try:
        table.put_item(Item=data)
        return {'statusCode': 201, 'body': 'Created'}
    except (BotoCoreError, ClientError) as error:
        return {'statusCode': 400, 'body': str(error)}

def read(event):
    try:
        response = table.get_item(Key={'id': event['pathParameters']['id']})
        item = response['Item']
        return {'statusCode': 200, 'body': json.dumps(item)}
    except (BotoCoreError, ClientError) as error:
        return {'statusCode': 400, 'body': str(error)}

def update(event):
    data = json.loads(event['body'])
    try:
        table.update_item(Key={'id': event['pathParameters']['id']}, AttributeUpdates=data)
        return {'statusCode': 200, 'body': 'Updated'}
    except (BotoCoreError, ClientError) as error:
        return {'statusCode': 400, 'body': str(error)}

def delete(event):
    try:
        table.delete_item(Key={'id': event['pathParameters']['id']})
        return {'statusCode': 200, 'body': 'Deleted'}
    except (BotoCoreError, ClientError) as error:
        return {'statusCode': 400, 'body': str(error)}
