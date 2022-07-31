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
    print(f"event: {event}")
    print(f"context: {context}")

    print("Get Ingredients...")
    connection = db_connect()
    cursor = connection.cursor()
    print("Connected to database")

    if not event['pathParameters']['recipeid']:
        return {
            'statusCode': 400,
            'message': json.dumps('recipeid is missing')
        }
    recipeId = event['pathParameters']['recipeid']
    print(f"recipeId: {recipeId}")

    # Retrieve and organize the ingredients
    cursor.execute(f'SELECT * FROM recipes_db.ingredients WHERE recipeId = {recipeId}')
    ingredientsSql = cursor.fetchall()
    print(f"sql response: {ingredientsSql}")
    if not ingredientsSql:
        print("recipeId does not exist")
        return {
            'statusCode': 204,
            'headers': {
                'Access-Control-Allow-Origin' : '*',
                'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Credentials' : 'true',
                'Content-Type': 'application/json'
            },
        }
    
    ingredientsList = []
    for ingredient in ingredientsSql:
        ingredientDict = {}
        ingredientDict['ingredientName'] = ingredient[1]
        ingredientDict['ingredientAmount'] = ingredient[2]
        ingredientDict['ingredientUnit'] = ingredient[3]
        ingredientsList.append(ingredientDict)

    print(f"ingredients: {ingredientsList}")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials' : 'true',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'ingredients': ingredientsList
        })
    }
