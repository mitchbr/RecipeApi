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
        print("No content to show")
        return {
            'statusCode': 204
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
        'body': json.dumps({
            'ingredients': ingredientsList
        })
    }
