import boto3
from boto3.dynamodb.types import TypeDeserializer
td = TypeDeserializer()
import json

"""
    POST endpoint
    Add a new author
"""
def lambda_handler(event, context):
    print(f"event: {event}")
    if "username" not in event:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "username missing from body"
            })
        }

    dynamodb = boto3.client("dynamodb", region_name="us-east-2")
    print(f"Connected to dynamoDB: {dynamodb}")

    check_res = dynamodb.get_item(TableName="recipe_authors", Key={"username": {"S": event["username"]}})
    print(f"dynamodb.get_item: {check_res}")
    if "Item" in check_res:
        return {
            "statusCode": 409,
            "body": json.dumps({
                "message": "username exists"
            })
        }

    serial_item={"username": {"S": event["username"]}, "following": {"L": []}}
    add_res = dynamodb.put_item(TableName="recipe_authors", Item=serial_item)
    print(f"dynamodb.put_item: {add_res}")

    if add_res["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "DynamoDB Could not add item"
            })
        }
    
    item = {}
    for key in serial_item:
        item[key] = td.deserialize(serial_item[key])
    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }