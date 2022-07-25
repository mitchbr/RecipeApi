import boto3
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
td = TypeDeserializer()
import json

from database.db_connect import db_connect

"""
    GET endpoint
    Return all data for an author by ID
"""
def lambda_handler(event, context):
    print(f"event: {event}")
    if event['pathParameters']['username']:
        username = event['pathParameters']['username']
    else:
        return {
        'statusCode': 400,
        'body': json.dumps('Missing username')
    }
    print(f"Author get username: {username}")

    dynamodb = boto3.client('dynamodb', region_name='us-east-2')
    print(f"Connected to dynamoDB: {dynamodb}")

    db_res = dynamodb.get_item(TableName='recipe_authors', Key={'username': {"S": username}})
    user = {}
    for key in db_res['Item']:
        user[key] = td.deserialize(db_res['Item'][key])
    print(f"user: {user}")
    
    return {
        'statusCode': 200,
        'body': json.dumps(user)
    }