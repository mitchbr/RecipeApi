import json

"""
    DELETE endpoint
    Remove a recipe
"""
def delRecipe(connection, event):
    recipe = json.loads(event["body"])
    if "recipeId" not in recipe:
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
        return {
            'statusCode': 204,
            'message': f'recipeId {recipe["recipeId"]} not found in database'
        }

    # Delete ingredient data
    cursor.execute(
        f'DELETE FROM recipes_db.ingredients WHERE recipeID = {recipe["recipeId"]}'
    )
    connection.commit()

    # Delete image data
    cursor.execute(
        f'DELETE FROM recipes_db.images WHERE recipeID = {recipe["recipeId"]}'
    )
    connection.commit()

    # Delete recipe data
    cursor.execute(
        f'DELETE FROM recipes_db.recipes WHERE recipeID = {recipe["recipeId"]}'
    )
    connection.commit()
    
    return {
        'statusCode': 200,
        'message': json.dumps(f'Successfully deleted {deletedName[0]} from the database'),
    }