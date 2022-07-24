import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:intl/intl.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/services.dart';
import 'dart:io';

import 'recipe.dart';
import 'package:recipe_api/components/add_edit_recipe_components/add_edit_recipe_metadata.dart';

class RecipeDetails extends StatefulWidget {
  final Recipe recipeEntry;
  final Uint8List image;
  const RecipeDetails({Key? key, required this.recipeEntry, required this.image}) : super(key: key);

  @override
  _RecipeDetailsState createState() => _RecipeDetailsState();
}

class _RecipeDetailsState extends State<RecipeDetails> {
  _RecipeDetailsState();

  late Recipe recipeEntry;
  late List<bool> checkedValues;
  late Uint8List entryImage;

  @override
  void initState() {
    super.initState();
    recipeEntry = widget.recipeEntry;
    recipeEntry.ingredients = []; // TODO: Remove this after testing
    fetchIngredients(recipeEntry.recipeId);
    entryImage = widget.image;
  }

  Future<void> fetchIngredients(recipeId) async {
    final String jsonData = await rootBundle.loadString('assets/api_url.json');
    final apiUrl = await json.decode(jsonData);
    final res = await http.get(
      Uri.parse('${apiUrl['url']}/ingredients/$recipeId'),
    );

    if (res.statusCode == 200) {
      setState(() {
        recipeEntry.ingredients = jsonDecode(res.body)["ingredients"];
        checkedValues = List.filled(recipeEntry.ingredients.length, true, growable: false);
      });
    } else {
      throw Exception('Failed to load recipes');
    }
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
                context: context, builder: (BuildContext context) => verifyDeleteRecipe(context, recipeEntry)),
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
              SizedBox(
                child: Image.memory(entryImage),
                height: 400,
              ),
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
    Navigator.push(
            context,
            MaterialPageRoute(
                builder: (context) => AddEditRecipeMetadata(recipeData: recipeEntry, recipeImage: entryImage)))
        .then((data) => setState(() => {}));
  }

  Widget verifyDeleteRecipe(BuildContext context, Recipe recipeData) {
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
              deleteRecipe(recipeData);
            },
            child: const Text('Yes'),
          ),
        ]);
  }

  void deleteRecipe(Recipe recipeData) async {
    // TODO: Verify response code
    // Delete recipe data
    final String jsonData = await rootBundle.loadString('assets/api_url.json');
    final apiUrl = await json.decode(jsonData);
    await http.delete(Uri.parse('${apiUrl['url']}/recipes'),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode({'recipeId': recipeData.recipeId}));

    // Delete recipe image
    final imageName = "${recipeData.recipeName}_${recipeData.author}.jpeg";
    var request = http.delete(Uri.parse(
        'https://0rbzt2fsha.execute-api.us-east-2.amazonaws.com/dev/images/mitchell-recipe-images/$imageName'));

    setState(() {
      Navigator.of(context).pop();
    });
  }
}
