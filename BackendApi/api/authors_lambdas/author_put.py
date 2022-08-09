import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
td = TypeDeserializer()
ts = TypeSerializer()
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

    check_user = dynamodb.get_item(TableName="recipe_authors", Key={"username": {"S": event["username"]}})
    print(f"dynamodb.get_item: {check_user}")
    if "Item" not in check_user:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "username does not exist"
            })
        }

    check_update = dynamodb.get_item(TableName="recipe_authors", Key={"username": {"S": event["update"]}})
    print(f"dynamodb.get_item: {check_update}")
    if "Item" not in check_update:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"cannot follow {event['update']}, user does not exist"
            })
        }    

    if ("following" in check_update["Item"]):
        following = td.deserialize(check_update["Item"]["following"])
    else:
        following = []
    print(f"following: {following}")

    if event["type"] == "follow" and event["update"] not in following:
        following.append(event["update"])
    elif event["type"] == "follow":
        return {
            "statusCode": 409,
            "body": json.dumps({
                "message": f"user already follows: {event['update']}"
            })
        }
    elif event["type"] == "unfollow" and event["update"] in following:
        following.remove(event["update"])
    elif event["type"] == "unfollow":
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"user does not follow: {event['update']}"
            })
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "bad request"
            })
        }

    serialized = []
    for item in following:
        serialized.append({'S': item})
    print(f"serialized: {serialized}")

    serial_item={"username": {"S": event["username"]}, "following": {"L": serialized}}
    update_res = dynamodb.update_item(
        TableName="recipe_authors",
        Key={
            "username": {"S": event["username"]}
        },
        UpdateExpression="set following = :r",
        ExpressionAttributeValues={
            ':r': {"L": serialized},
        },
        ReturnValues="UPDATED_NEW"
    )
    print(f"dynamodb.update_item: {update_res}")

    if update_res["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "DynamoDB Could not update item"
            })
        }
    
    item = {}
    for key in serial_item:
        item[key] = td.deserialize(serial_item[key])
    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }