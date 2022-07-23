import json

from db_connect import db_connect

"""
    POST endpoint
    Add a new recipe
"""
def lambda_handler(event, context):
    print("Adding Recipe...")
    connection = db_connect()
    cursor = connection.cursor()
    print("connected to database")
    newRecipe = event
    print(f"event: {event}")

    # Check if any keys are missing
    req_keys = ["recipeName", "instructions", "author", "category", "ingredients"]
    for key in req_keys:
        if key not in newRecipe:
            print(f"Fixing missing dict key: {key}")
            if key == "ingredients":
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
        print("ERROR: Author already has a recipe with this name")
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
    print("Recipe data added successfully")

    # Post ingredient data next
    ingredients = newRecipe["ingredients"]
    for ingredient in ingredients:
        cursor.execute(
            f'INSERT INTO recipes_db.ingredients(ingredientName, amount, unit, recipeID)'
            f'VALUES ("{ingredient["ingredientName"]}", "{ingredient["ingredientAmount"]}", "{ingredient["ingredientUnit"]}",'
            f'(SELECT recipeID FROM recipes_db.recipes WHERE recipeName = "{newRecipe["recipeName"]}" AND author = "{newRecipe["author"]}"));'
        )
        connection.commit()
        print(f"Ingredient data added successfully: {ingredient['ingredientName']}")

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
        
    print(f"recipe added: {newRecipeDb}")
    return {
        'statusCode': 200,
        'message': 'Successfully added to database',
        'body': json.dumps({"recipeId": newRecipeDb[0],
                            "recipeName": newRecipeDb[1],
                            "instructions": newRecipeDb[2],
                            "author": newRecipeDb[3],
                            "publishDate": newRecipeDb[4].strftime("%m-%d-%Y"),
                            "category": newRecipeDb[5],
                            "ingredients": ingredientRes})
    }
