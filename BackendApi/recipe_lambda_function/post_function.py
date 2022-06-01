import json

from recipe_lambda_function.lambda_function import db_connect

"""
    POST endpoint
    Add a new recipe
"""
def lambda_handler(event, context):
    connection = db_connect()
    cursor = connection.cursor()
    newRecipe = json.loads(event["body"])

    # Check if any keys are missing
    req_keys = ["recipeName", "instructions", "author", "category", "ingredients", "images"]
    for key in req_keys:
        if key not in newRecipe:
            if key == "ingredients" or key == "images":
                newRecipe[key] = []
            else:
                newRecipe[key] = ""

    
    cursor = connection.cursor()

    # Verify this author hasn't already posted a recipe with this name
    cursor.execute(
        f'SELECT recipeID FROM recipes_db.recipes WHERE recipeName = "{newRecipe["recipeName"]}" AND author = "{newRecipe["author"]}";'
    )
    duplicate_check = cursor.fetchall()
    if duplicate_check:
        return {
            'statusCode': 409,
            'message': f'Recipe with name {newRecipe["recipeName"]} and author {newRecipe["author"]}, already exists in database'
        }

    # Post the recipe data first
    cursor.execute(
        f'INSERT INTO recipes_db.recipes(recipeName, instructions, author, publishDate, category)'
        f'VALUES ("{newRecipe["recipeName"]}", "{newRecipe["instructions"]}", "{newRecipe["author"]}", CURDATE(), "{newRecipe["category"]}");'
    )
    connection.commit()

    # Post ingredient data next
    ingredients = newRecipe["ingredients"]
    for ingredient in ingredients:
        cursor.execute(
            f'INSERT INTO recipes_db.ingredients(ingredientName, amount, unit, recipeID)'
            f'VALUES ("{ingredient["ingredientName"]}", "{ingredient["ingredientAmount"]}", "{ingredient["ingredientUnit"]}",'
            f'(SELECT recipeID FROM recipes_db.recipes WHERE recipeName = "{newRecipe["recipeName"]}" AND author = "{newRecipe["author"]}"));'
        )
        connection.commit()
    
    # Post image data
    images = newRecipe["images"]
    for image in images:
        cursor.execute(
            f'INSERT INTO recipes_db.images(imageURL, recipeID)'
            f'VALUES ("{image}", (SELECT recipeID FROM recipes_db.recipes WHERE recipeName = "{newRecipe["recipeName"]}" AND author = "{newRecipe["author"]}"));'
        )
        connection.commit()

    # GET the new data posted to the DB
    cursor.execute(
        f'SELECT * FROM recipes_db.recipes WHERE recipeName = "{newRecipe["recipeName"]}" AND author = "{newRecipe["author"]}";'
    )
    newRecipeDb = cursor.fetchall()[0]

    # Get ingredient data
    cursor.execute(
        f'SELECT * FROM recipes_db.ingredients WHERE recipeID = {newRecipeDb[0]};'
    )
    newRecipeIngredients = cursor.fetchall()
    ingredientRes = []
    for ingredient in newRecipeIngredients:
        ingredientRes.append({"ingredientName": ingredient[1],
                            "ingredientAmount": ingredient[2],
                            "ingredientUnit": ingredient[3]})
        
    # Get image data
    cursor.execute(
        f'SELECT * FROM recipes_db.images WHERE recipeID = {newRecipeDb[0]};'
    )
    newRecipeImages = cursor.fetchall()
    imageRes = []
    for image in newRecipeImages:
        imageRes.append(image[1])

    return {
        'statusCode': 200,
        'message': 'Successfully added to database',
        'body': json.dumps({"recipeId": newRecipeDb[0],
                            "recipeName": newRecipeDb[1],
                            "instructions": newRecipeDb[2],
                            "author": newRecipeDb[3],
                            "publishDate": newRecipeDb[4].strftime("%m-%d-%Y"),
                            "category": newRecipeDb[5],
                            "ingredients": ingredientRes,
                            "images": imageRes})
    }
