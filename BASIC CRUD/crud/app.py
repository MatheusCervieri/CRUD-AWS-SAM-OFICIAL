import json

items = {}

def lambda_handler(event, context):
    print("Chegou na lambda")
    path = event['path']
    item_id = event['pathParameters']['id']

    if path == '/items' and event['httpMethod'] == 'GET':
        return get_all_items()
    elif path == '/items' and event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        return create_item(body)
    elif path == f'/items/{item_id}' and event['httpMethod'] == 'GET':
        return get_item(item_id)
    elif path == f'/items/{item_id}' and event['httpMethod'] == 'PUT':
        body = json.loads(event['body'])
        return update_item(item_id, body)
    elif path == f'/items/{item_id}' and event['httpMethod'] == 'DELETE':
        return delete_item(item_id)
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Invalid path'),
            'headers': {'Content-Type': 'application/json'}
        }
    
def get_all_items():
    return {
        'statusCode': 200,
        'body': json.dumps(list(items.values())),
        'headers': {'Content-Type': 'application/json'}
    }

def get_item(item_id):
    if item_id in items:
        return {
            'statusCode': 200,
            'body': json.dumps(items[item_id]),
            'headers': {'Content-Type': 'application/json'}
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Item not found'),
            'headers': {'Content-Type': 'application/json'}
        }

def create_item(item):
    item_id = str(len(items) + 1)
    item['id'] = item_id
    items[item_id] = item
    return {
        'statusCode': 201,
        'body': json.dumps(item),
        'headers': {'Content-Type': 'application/json'}
    }

def update_item(item_id, updated_item):
    if item_id in items:
        updated_item['id'] = item_id
        items[item_id] = updated_item
        return {
            'statusCode': 200,
            'body': json.dumps(updated_item),
            'headers': {'Content-Type': 'application/json'}
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Item not found'),
            'headers': {'Content-Type': 'application/json'}
        }

def delete_item(item_id):
    if item_id in items:
        del items[item_id]
        return {
            'statusCode': 204,
            'body': '',
            'headers': {'Content-Type': 'application/json'}
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Item not found'),
            'headers': {'Content-Type': 'application/json'}
        }
