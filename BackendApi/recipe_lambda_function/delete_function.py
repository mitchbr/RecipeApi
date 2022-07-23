import json

from db_connect import db_connect

"""
    DELETE endpoint
    Remove a recipe
"""
def lambda_handler(event, context):
    print("Deleting Recipe...")
    connection = db_connect()
    cursor = connection.cursor()
    print("connected to database")
    recipe = event
    print(f"event: {event}")

    if "recipeId" not in recipe:
        print("ERROR: recipeId not in request")
        return {
            'statusCode': 400,
            'message': f'recipeId required to delete'
        }
    
    cursor = connection.cursor()
    
    # Get the recipe name to let the user know what's been deleted
    cursor.execute(
        f'''SELECT recipeName
        FROM recipes_db.recipes
        WHERE recipeID = {recipe["recipeId"]}'''
    )
    deletedName = cursor.fetchall()
    if not deletedName:
        print("recipeId does not exist in DB")
        return {
            'statusCode': 204,
            'message': f'recipeId {recipe["recipeId"]} not found in database'
        }

    # Delete ingredient data
    cursor.execute(
        f'DELETE FROM recipes_db.ingredients WHERE recipeID = {recipe["recipeId"]}'
    )
    connection.commit()
    print("Successfully deleted ingredient data")

    # Delete recipe data
    cursor.execute(
        f'DELETE FROM recipes_db.recipes WHERE recipeID = {recipe["recipeId"]}'
    )
    connection.commit()
    print(f"Successfully deleted {deletedName[0]} from the database")
    
    return {
        'statusCode': 200,
        'message': json.dumps(f'Successfully deleted {deletedName[0]} from the database'),
    }