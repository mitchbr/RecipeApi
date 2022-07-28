import 'package:intl/intl.dart';

class Recipe {
  late int recipeId;
  late String recipeName;
  late String instructions;
  late String author;
  late DateTime publishDate;
  late String category;
  late List ingredients;

  Recipe({
    required this.recipeId,
    required this.recipeName,
    required this.instructions,
    required this.author,
    required this.publishDate,
    required this.category,
    required this.ingredients,
  });

  factory Recipe.fromJson(Map<String, dynamic> json) {
    DateFormat dateFormat = DateFormat("MM-dd-yyyy");
    return Recipe(
        recipeId: json["recipeId"],
        recipeName: json["recipeName"],
        instructions: json["instructions"],
        author: json["author"],
        publishDate: dateFormat.parse(json["publishDate"]),
        category: json["category"],
        ingredients: []);
  }

  Map<String, dynamic> toJson() {
    DateFormat dateFormat = DateFormat("MM-dd-yyyy");
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data["recipeId"] = recipeId;
    data["recipeName"] = recipeName;
    data["instructions"] = instructions;
    data["author"] = author;
    data["publishDate"] = dateFormat.format(publishDate);
    data["category"] = category;
    data["ingredients"] = ingredients;
    return data;
  }
}
