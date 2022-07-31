import json

from database.db_connect import db_connect

"""
    GET endpoint
    Return all data for all recipes
"""
def lambda_handler(event, context):
    print("Get Recipes...")
    print(f"event: {event}")
    connection = db_connect()
    cursor = connection.cursor()
    print("Connected to database")

    offset = 0
    if (event['queryStringParameters']['offset']):
        offset = int(event['queryStringParameters']['offset'])

    print(f"offset: {offset}")

    # Get primary recipe data and organize it into a list
    cursor.execute(
        f'''SELECT * FROM recipes_db.recipes
        ORDER BY recipeId DESC
        LIMIT 10 OFFSET {offset};
        ''')
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