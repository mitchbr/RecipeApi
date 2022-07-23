-- Insert into recipes table
INSERT INTO recipes_db.recipes (recipeName, instructions, author, publishDate, category)
VALUES ("Butter Chicken", "Cook some stuff", "Mitchell", CURDATE(), "Entree");

-- Insert into ingredients table
INSERT INTO recipes_db.ingredients (ingredientName, amount, unit, recipeID)
VALUES ("Chicken", "2", "lbs", (SELECT recipeID FROM recipes_db.recipes WHERE recipeName = "Butter Chicken"));