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

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Visitor Counter</title>
        <style>
            body {{
                margin: 0;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #1e1e2f, #2d2d44);
                font-family: 'Segoe UI', system-ui, sans-serif;
            }}
            .card {{
                background: #ffffff10;
                backdrop-filter: blur(10px);
                border: 1px solid #ffffff20;
                border-radius: 20px;
                padding: 48px 64px;
                text-align: center;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }}
            .label {{
                color: #a0a0c0;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin-bottom: 8px;
            }}
            .count {{
                color: #ffffff;
                font-size: 72px;
                font-weight: 700;
                background: linear-gradient(90deg, #7c3aed, #06b6d4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .footer {{
                color: #6b6b8a;
                font-size: 12px;
                margin-top: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="label">Visitantes</div>
            <div class="count">{count}</div>
            <div class="footer">AWS Lambda + DynamoDB • Serverless</div>
        </div>
    </body>
    </html>
    """

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'text/html'
        },
        'body': html
    }