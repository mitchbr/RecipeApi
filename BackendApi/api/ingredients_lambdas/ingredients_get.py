import json

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from database import db_connect

"""
    GET endpoint
    Return all ingredient data for a recipe
"""
def lambda_handler(event, context):
    print("Get Ingredients...")
    connection = db_connect()
    cursor = connection.cursor()
    print("Connected to database")
    print(f"event: {event}")
    ingredients = event

    return {
        'statusCode': 200,
        'body': ingredients
    }
