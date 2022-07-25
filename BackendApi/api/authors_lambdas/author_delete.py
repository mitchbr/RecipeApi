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
    if not event["pathParameters"]["username"]:
        return {
        "statusCode": 400,
        "body": json.dumps("Missing username")
    }
    username = event["pathParameters"]["username"]
    print(f"Author get username: {username}")

    dynamodb = boto3.client("dynamodb", region_name="us-east-2")
    print(f"Connected to dynamoDB: {dynamodb}")

    check_res = dynamodb.get_item(TableName="recipe_authors", Key={"username": {"S": username}})
    print(f"dynamodb.get_item: {check_res}")
    if "Item" not in check_res:
        return {
            "statusCode": 409,
            "body": json.dumps({
                "message": "username does not exist"
            })
        }

    delete_res = dynamodb.delete_item(TableName="recipe_authors", Key={"username": {"S": username}})
    print(f"dynamo response: {delete_res}")

    if delete_res["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return {
            "statusCode": 400,
            "body": json.dumps("DynamoDB Could not remove item")
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Successfully removed {username}"
        })
    }