import json

"""
    GET endpoint
    Return all data for all recipes
"""
def getRecipes(connection):
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


    # Retrieve and organize the images
    cursor.execute(f'SELECT * FROM recipes_db.images')
    imagesSql = cursor.fetchall()
    imagesDict = {}
    for row in imagesSql:
        if row[2] not in imagesSql:
            # Create a new list for a new recipe
            imagesDict[row[2]] = [row[1]]
        else:
            # Add an image to an existing recipe
            imagesDict[row[2]].append(row[1])


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

        # return empty array if there are no images
        if row[2] not in imagesDict:
            imagesResponse = []
        else:
            imagesResponse = ingredientsDict[row[0]]

        recipesList.append({"recipeId": row[0],
                            "recipeName": row[1],
                            "instructions": row[2],
                            "author": row[3],
                            "publishDate": row[4].strftime("%m-%d-%Y"),
                            "category": row[5],
                            "ingredients": ingredientsResponse,
                            "images": imagesResponse})

    return {
        'statusCode': 200,
        'body': json.dumps({"recipes": recipesList})
    }