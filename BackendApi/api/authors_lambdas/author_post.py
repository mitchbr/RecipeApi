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

    dynamodb = boto3.client('dynamodb', region_name='us-east-2')
    print(f"Connected to dynamoDB: {dynamodb}")

    serial_item={'username': {"S": event['username']}, 'following': {"L": []}}
    res = dynamodb.put_item(TableName='recipe_authors', Item=serial_item)
    print(f"dynamo response: {res}")

    if res["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return {
            'statusCode': 400,
            'body': json.dumps("DynamoDB Could not add item")
        }
    
    item = {}
    for key in serial_item:
        item[key] = td.deserialize(serial_item[key])
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }