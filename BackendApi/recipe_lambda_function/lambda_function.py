import json
import os
import boto3
import pymysql
from get_function import getRecipes
from post_function import postRecipe
from put_function import putRecipe
from delete_function import delRecipe


# Create the paths for the four requests
DEFAULT_RAW_PATH = "/"
GET_RAW_PATH = "/getRecipes"
CREATE_RAW_PATH = "/createRecipe"
PUT_RAW_PATH = "/updateRecipe"
DELETE_RAW_PATH = "/deleteRecipe"


"""
    Main API entrypoint
"""
def lambda_handler(event, context):
    connection = db_connect()

    if event["rawPath"] == DEFAULT_RAW_PATH:
        return {
            'statusCode': 200,
            'body': json.dumps('got data!')
        }
    elif event["rawPath"] == GET_RAW_PATH:
        return getRecipes(connection)
    elif event["rawPath"] == CREATE_RAW_PATH:
        return postRecipe(connection, event)
    elif event["rawPath"] == PUT_RAW_PATH:
        return putRecipe(connection, event)
    elif event["rawPath"] == DELETE_RAW_PATH:
        return delRecipe(connection, event)
    else:
        return {
            'statuscode': 404,
            'body': json.dumps('Please enter a proper endpoint')
        }

def db_connect():
    if os.path.exists("creds.json"):
        # Local testing
        with open("creds.json") as f:
            creds = json.load(f)

        endpoint = creds["endpoint"]
        username = creds["username"]
        password = creds["pass"]
        dbName = creds["db_name"]
    else:
        pass
        # Get secrets information
        secrets_client = boto3.client('secretsmanager')
        secret_arn = 'arn:aws:secretsmanager:us-east-2:369135786923:secret:RecipeDbAccess-qYKVSd'
        auth_token = secrets_client.get_secret_value(SecretId=secret_arn).get('SecretString')
        auth_json = json.loads(auth_token)

        endpoint = auth_json["host"]
        username = auth_json["username"]
        password = auth_json["password"]
        dbName = "recipes_db"

    # Connect to DB
    return pymysql.connect(host=endpoint, user=username, passwd=password, db=dbName)

