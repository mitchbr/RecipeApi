import os
import json
import boto3
import pymysql

def db_connect():
    if os.path.exists("creds.json"):
        print("WARNING: Using local credentials...")
        # Local testing
        with open("creds.json") as f:
            creds = json.load(f)

        endpoint = creds["endpoint"]
        username = creds["username"]
        password = creds["pass"]
        dbName = creds["db_name"]
    else:
        print("Using secrets manager credentials...")
        # Get secrets information
        secrets_client = boto3.client('secretsmanager')
        secret_arn = 'arn:aws:secretsmanager:us-east-2:369135786923:secret:RecipeDbAccess-qYKVSd'
        auth_token = secrets_client.get_secret_value(SecretId=secret_arn).get('SecretString')
        auth_json = json.loads(auth_token)

        endpoint = auth_json["host"]
        username = auth_json["username"]
        password = auth_json["password"]
        dbName = "recipes_db"

    print(f"Connecting to database: {dbName}")
    # Connect to DB
    return pymysql.connect(host=endpoint, user=username, passwd=password, db=dbName)