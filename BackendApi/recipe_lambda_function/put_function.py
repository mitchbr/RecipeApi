import json

from db_connect import db_connect

"""
    PUT endpoint
    Update a recipe's data
"""
def lambda_handler(event, context):
    connection = db_connect()
    cursor = connection.cursor()
    recipe = event

    if "recipeId" not in recipe:
        return {
        'statusCode': 400,
        'message': 'Please provide a recipeId'
    }

    # Check if any keys are missing
    req_keys = ["recipeName", "instructions", "author", "category"]
    for key in req_keys:
        if key not in recipe:
            recipe[key] = ""
    
    cursor = connection.cursor()

    # Update recipe data
    cursor.execute(
        f'''UPDATE recipes_db.recipes
        SET recipeName = "{recipe["recipeName"]}", instructions = "{recipe["instructions"]}", author = "{recipe["author"]}", category = "{recipe["category"]}"
        WHERE recipeID = {recipe["recipeId"]}'''
    )
    connection.commit()

    # Update ingredient data
    if "ingredients" in recipe:
        updateIngredients(connection, cursor, recipe)
        
    return {
        'statusCode': 200,
        'message': 'Successfully updated recipe',
        'body': json.dumps(recipe)
    }

def updateIngredients(connection, cursor, recipe):
    # TODO: Make this happen without delete/post
    cursor.execute(
        f'DELETE FROM recipes_db.ingredients WHERE recipeID = {recipe["recipeId"]}'
    )
    connection.commit()

    ingredients = recipe["ingredients"]
    for ingredient in ingredients:
        cursor.execute(
            f'INSERT INTO recipes_db.ingredients(ingredientName, amount, unit, recipeID)'
            f'VALUES ("{ingredient["ingredientName"]}", "{ingredient["ingredientAmount"]}", "{ingredient["ingredientUnit"]}",'
            f'(SELECT recipeID FROM recipes_db.recipes WHERE recipeName = "{recipe["recipeName"]}" AND author = "{recipe["author"]}"))'
        )
        connection.commit()
