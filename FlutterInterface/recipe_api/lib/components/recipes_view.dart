import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/services.dart';

import 'recipe.dart';
import 'recipe_details.dart';
import 'package:recipe_api/components/add_edit_recipe_components/add_edit_recipe_metadata.dart';

class RecipesView extends StatefulWidget {
  const RecipesView({Key? key}) : super(key: key);

  @override
  State<RecipesView> createState() => _RecipesViewState();
}

class _RecipesViewState extends State<RecipesView> {
  List recipeEntries = [];
  bool loadedSql = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: bodyBuilder(context),
        floatingActionButton:
            FloatingActionButton(onPressed: () => pushNewEntry(context), child: const Icon(Icons.add)));
  }

  void fetchRecipes() async {
    final String jsonData = await rootBundle.loadString('assets/api_url.json');
    final apiUrl = await json.decode(jsonData);
    final res = await http.get(
      Uri.parse('${apiUrl['url']}/recipes'),
    );

    if (res.statusCode == 200) {
      final entriesJson = jsonDecode(jsonDecode(res.body)["body"])["recipes"];
      final entriesList = entriesJson.map((recipe) => Recipe.fromJson(recipe)).toList();

      setState(() {
        loadedSql = true;
        recipeEntries = entriesList;
      });
    } else {
      throw Exception('Failed to load recipes');
    }
  }

  /*
   *
   * Page Views
   * 
   */
  Widget bodyBuilder(BuildContext context) {
    fetchRecipes();
    if (recipeEntries.isEmpty && !loadedSql) {
      return circularIndicator(context);
    } else if (recipeEntries.isEmpty) {
      return emptyWidget(context);
    } else {
      return entriesList(context);
    }
  }

  Widget emptyWidget(BuildContext context) {
    return const Center(
        child: Icon(
      Icons.book,
      size: 100,
    ));
  }

  Widget circularIndicator(BuildContext context) {
    return const Center(child: CircularProgressIndicator());
  }

/*
   *
   * Recipes ListView
   * 
   */
  Widget entriesList(BuildContext context) {
    return ListView.builder(
        itemCount: recipeEntries.length,
        itemBuilder: (context, index) {
          return groceryTile(index);
        });
  }

  Widget groceryTile(int index) {
    return ListTile(
      title: Text('${recipeEntries[index].recipeName}'),
      onTap: () => pushRecipeDetails(context, recipeEntries[index]),
    );
  }

  /*
   *
   * Paths for Different Pages
   * 
   */
  void pushNewEntry(BuildContext context) {
    Navigator.push(
            context,
            MaterialPageRoute(
                builder: (context) => const AddEditRecipeMetadata())) // TODO: CHange back to: AddEditRecipeMetadata
        .then((data) => setState(() => {}));
  }

  void pushRecipeDetails(BuildContext context, recipeEntry) {
    Navigator.push(context, MaterialPageRoute(builder: (context) => RecipeDetails(recipeEntry: recipeEntry)))
        .then((data) => setState(() => {}));
  }
}
