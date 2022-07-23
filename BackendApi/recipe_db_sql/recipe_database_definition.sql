-- Drop tables to reset schema
DROP TABLE IF EXISTS recipes_db.ingredients;
DROP TABLE IF EXISTS recipes_db.recipes;

-- Create the recipes table
CREATE TABLE recipes_db.recipes (
	recipeID int AUTO_INCREMENT NOT NULL,
    recipeName varchar(255) NOT NULL,
    instructions varchar(255) NOT NULL,
    author varchar(255) NOT NULL,
    publishDate DATE NOT NULL,
    category varchar(255) NOT NULL,
    image varchar(255) NOT NULL,
    PRIMARY KEY (recipeID)
);
    
-- Create ingredients table -> recipeID ties to recipes table
CREATE TABLE recipes_db.ingredients (
	ingredientID int AUTO_INCREMENT NOT NULL,
    ingredientName varchar(255) NOT NULL,
    amount varchar(255) NOT NULL,
    unit varchar(255) NOT NULL,
    recipeID int NOT NULL,
    PRIMARY KEY (ingredientID),
    FOREIGN KEY (recipeID) REFERENCES recipes_db.recipes (recipeID)
);
