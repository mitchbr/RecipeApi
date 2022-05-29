To invoke this API, use the following links:

 - GET Request: https://59odijjmkg.execute-api.us-east-2.amazonaws.com/getRecipes

 - POST Request: https://59odijjmkg.execute-api.us-east-2.amazonaws.com/createRecipe

    - Required Parameters:
        - name: The name of the recipe you are creating

 - PUT Request: https://59odijjmkg.execute-api.us-east-2.amazonaws.com/addIngredient
 
    - Required Parameters:
        - name: The name of the recipe you are adding ingredients to
        - ingredient: The ingredient to add to the recipe

 - DELETE Request: https://59odijjmkg.execute-api.us-east-2.amazonaws.com/deleteRecipe

    - Required Parameters:
        - name: The name of the recipe you are removing

