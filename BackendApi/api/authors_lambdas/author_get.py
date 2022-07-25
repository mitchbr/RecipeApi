import boto3
from boto3.dynamodb.types import TypeDeserializer
td = TypeDeserializer()
import json

"""
    GET endpoint
    Return all data for an author by ID
"""
def lambda_handler(event, context):
    print(f"event: {event}")
    if not event['pathParameters']['username']:
        return {
        'statusCode': 400,
        'body': json.dumps('Missing username')
    }
    username = event['pathParameters']['username']
    print(f"Author get username: {username}")

    dynamodb = boto3.client('dynamodb', region_name='us-east-2')
    print(f"Connected to dynamoDB: {dynamodb}")

    res = dynamodb.get_item(TableName='recipe_authors', Key={'username': {"S": username}})
    user = {}
    for key in res['Item']:
        user[key] = td.deserialize(res['Item'][key])
    print(f"user: {user}")
    
    return {
        'statusCode': 200,
        'body': json.dumps(user)
    }