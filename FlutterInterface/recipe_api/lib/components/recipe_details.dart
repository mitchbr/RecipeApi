import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:intl/intl.dart';
import 'package:http/http.dart' as http;
import 'package:recipe_api/components/add_edit_recipe_components/add_edit_recipe_metadata.dart';

import 'recipe.dart';

class RecipeDetails extends StatefulWidget {
  final Recipe recipeEntry;
  const RecipeDetails({Key? key, required this.recipeEntry}) : super(key: key);

  @override
  _RecipeDetailsState createState() => _RecipeDetailsState();
}

class _RecipeDetailsState extends State<RecipeDetails> {
  late Recipe recipeEntry;
  _RecipeDetailsState();

  late List<bool> checkedValues;

  @override
  void initState() {
    super.initState();
    recipeEntry = widget.recipeEntry;
    checkedValues = List.filled(recipeEntry.ingredients.length, true, growable: false);
  }

  /*
   *
   * Page Entry Point
   * 
   */
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(recipeEntry.recipeName), actions: [
        Builder(
          builder: (context) => IconButton(
            icon: const Icon(Icons.edit),
            onPressed: () => pushEditEntry(context),
          ),
        ),
        Builder(
          builder: (context) => IconButton(
            icon: const Icon(Icons.delete_rounded),
            onPressed: () => showDialog<String>(
                context: context, builder: (BuildContext context) => verifyDeleteRecipe(context, recipeEntry.recipeId)),
          ),
        ),
      ]),
      body: entriesList(context),
    );
  }

  /*
   *
   * Recipe Detail ListView
   * 
   */
  Widget entriesList(BuildContext context) {
    return ListView.builder(
        itemCount: recipeEntry.ingredients.length + 1,
        itemBuilder: (context, index) {
          if (index == recipeEntry.ingredients.length) {
            return recipeMetaData(recipeEntry);
          } else if (index == 0) {
            return Column(children: [
              const ListTile(
                  title: Text(
                'Ingredients',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              )),
              itemTile(index)
            ]);
          } else {
            return itemTile(index);
          }
        });
  }

  Widget recipeMetaData(recipeDetails) {
    DateFormat dateFormat = DateFormat("MMMM d, yyyy");
    return Column(children: [
      const ListTile(
          title: Text(
        'Instructions',
        style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
      )),
      ListTile(title: Text(recipeEntry.instructions)),
      const ListTile(
          title: Text(
        'Details',
        style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
      )),
      ListTile(title: Text('Author: ${recipeEntry.author}')),
      ListTile(title: Text('Date Published: ${dateFormat.format(recipeEntry.publishDate)}')),
      ListTile(title: Text('Category: ${recipeEntry.category}')),
      const ListTile(
          title: SizedBox(
        height: 20,
      ))
    ]);
  }

  Widget itemTile(int index) {
    var curIngredient = recipeEntry.ingredients[index];
    return StatefulBuilder(builder: (BuildContext context, StateSetter setState) {
      // TODO: Remove checkbox?
      return CheckboxListTile(
        title: Text('${curIngredient["ingredientName"]} '
            '(${curIngredient["ingredientAmount"]} '
            '${curIngredient["ingredientUnit"]})'),
        value: checkedValues[index],
        onChanged: (newValue) {
          setState(() {
            checkedValues[index] = newValue!;
          });
        },
        activeColor: Colors.teal,
        controlAffinity: ListTileControlAffinity.leading,
      );
    });
  }

  /*
   *
   * Delete and Edit Recipe
   * 
   */
  void pushEditEntry(BuildContext context) {
    Navigator.push(context, MaterialPageRoute(builder: (context) => AddEditRecipeMetadata(recipeData: recipeEntry)))
        .then((data) => setState(() => {}));
  }

  Widget verifyDeleteRecipe(BuildContext context, int id) {
    return AlertDialog(
        title: const Text('Delete Recipe?'),
        content: const Text('This will permenently remove the recipe'),
        actions: <Widget>[
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('No'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              deleteRecipe(id);
            },
            child: const Text('Yes'),
          ),
        ]);
  }

  void deleteRecipe(id) async {
    // TODO: Verify response code
    final http.Response response =
        await http.delete(Uri.parse('https://i4yiwtjkg7.execute-api.us-east-2.amazonaws.com/deleteRecipe'),
            headers: <String, String>{
              'Content-Type': 'application/json; charset=UTF-8',
            },
            body: jsonEncode({'recipeId': id}));

    setState(() {
      Navigator.of(context).pop();
    });
  }
}
