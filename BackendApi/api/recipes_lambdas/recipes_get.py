import json

from database.db_connect import db_connect

"""
    GET endpoint
    Return all data for all recipes
"""
def lambda_handler(event, context):
    print("Get Recipes...")
    connection = db_connect()
    cursor = connection.cursor()
    print("Connected to database")

    # Get primary recipe data and organize it into a list
    cursor.execute('SELECT * FROM recipes_db.recipes')
    recipeSql = cursor.fetchall()
    print(f"recipes: {recipeSql}")

    recipesList = []
    for row in recipeSql:
        recipesList.append({
            "recipeId": row[0],
            "recipeName": row[1],
            "instructions": row[2],
            "author": row[3],
            "publishDate": row[4].strftime("%m-%d-%Y"),
            "category": row[5],
        })
    print(f"recipesList: {recipesList}")    

    return {
        'statusCode': 200,
        'body': json.dumps({"recipes": recipesList})
    }