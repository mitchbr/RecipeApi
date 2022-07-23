import json

from db_connect import db_connect

"""
    GET endpoint
    Return all data for all recipes
"""
def lambda_handler(event, context):
    connection = db_connect()
    cursor = connection.cursor()

    # Retrieve and organize the ingredients
    cursor.execute(f'SELECT * FROM recipes_db.ingredients')
    ingredientsSql = cursor.fetchall()
    ingredientsDict = {}
    for row in ingredientsSql:
        if row[4] not in ingredientsDict:
            # Create a new dict for a new recipe
            ingredientsDict[row[4]] = [{"ingredientName": row[1],
                                        "ingredientAmount": row[2],
                                        "ingredientUnit": row[3]}]
        else:
            # Add an ingredient to an existing recipe
            ingredientsDict[row[4]].append({"ingredientName": row[1],
                                            "ingredientAmount": row[2],
                                            "ingredientUnit": row[3]})

    # Get primary recipe data and organize it into a list
    cursor.execute('SELECT * FROM recipes_db.recipes')
    recipeSql = cursor.fetchall()

    recipesList = []
    for row in recipeSql:
        # return empty array if there are no ingredients
        if row[0] not in ingredientsDict:
            ingredientsResponse = []
        else:
            ingredientsResponse = ingredientsDict[row[0]]

        recipesList.append({"recipeId": row[0],
                            "recipeName": row[1],
                            "instructions": row[2],
                            "author": row[3],
                            "publishDate": row[4].strftime("%m-%d-%Y"),
                            "category": row[5],
                            "ingredients": ingredientsResponse})

    return {
        'statusCode': 200,
        'body': json.dumps({"recipes": recipesList})
    }