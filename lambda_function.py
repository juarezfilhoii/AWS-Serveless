import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('visitor-counter')

def lambda_handler(event, context):
    path = event.get('rawPath', '/')

    if path != '/':
        return {
            'statusCode': 404,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': '{"error": "not found"}'
        }

    response = table.update_item(
        Key={'id': 'counter'},
        UpdateExpression='ADD #c :incr',
        ExpressionAttributeNames={'#c': 'count'},
        ExpressionAttributeValues={':incr': 1},
        ReturnValues='UPDATED_NEW'
    )
    count = int(response['Attributes']['count'])
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': f'{{"visits": {count}}}'
    }
