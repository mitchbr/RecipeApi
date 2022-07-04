import 'dart:io';
import 'dart:typed_data';

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
  List<Uint8List> images = [];
  bool loadedSql = false;

  @override
  void initState() {
    super.initState();
    fetchRecipes();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: RefreshIndicator(onRefresh: () => fetchRecipes(), child: bodyBuilder(context)),
        floatingActionButton:
            FloatingActionButton(onPressed: () => pushNewEntry(context), child: const Icon(Icons.add)));
  }

  Future<void> fetchRecipes() async {
    final String jsonData = await rootBundle.loadString('assets/api_url.json');
    final apiUrl = await json.decode(jsonData);
    final res = await http.get(
      Uri.parse('${apiUrl['url']}/recipes'),
    );

    if (res.statusCode == 200) {
      final entriesJson = jsonDecode(jsonDecode(res.body)["body"])["recipes"];
      final entriesList = entriesJson.map((recipe) => Recipe.fromJson(recipe)).toList();
      for (var i = 0; i < entriesList.length; i++) {
        images.add(await fetchRecipeImage(entriesList[i]));
      }

      setState(() {
        loadedSql = true;
        recipeEntries = entriesList;
      });
    } else {
      throw Exception('Failed to load recipes');
    }
  }

  Future<Uint8List> fetchRecipeImage(recipe) async {
    final String jsonData = await rootBundle.loadString('assets/api_url.json');
    final apiUrl = await json.decode(jsonData);
    final imageName = "${recipe.recipeName}_${recipe.author}.jpeg";
    var url = Uri.parse('${apiUrl['url']}/images/mitchell-recipe-images/$imageName');
    var res = await http.get(url);
    return res.bodyBytes;
  }

  /*
   *
   * Page Views
   * 
   */
  Widget bodyBuilder(BuildContext context) {
    if (recipeEntries.isEmpty && !loadedSql) {
      return circularIndicator(context);
    } else if (recipeEntries.isEmpty) {
      return emptyWidget(context);
    } else {
      return entriesList(context);
    }
  }

  Widget emptyWidget(BuildContext context) {
    return Center(child: IconButton(onPressed: () => fetchRecipes(), icon: Icon(Icons.refresh)));
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
      leading: Image.memory(images[index]),
      onTap: () => pushRecipeDetails(context, recipeEntries[index], images[index]),
    );
  }

  /*
   *
   * Paths for Different Pages
   * 
   */
  void pushNewEntry(BuildContext context) {
    Navigator.push(context, MaterialPageRoute(builder: (context) => const AddEditRecipeMetadata()))
        .then((data) => setState(() => {}));
  }

  void pushRecipeDetails(BuildContext context, recipeEntry, image) {
    Navigator.push(
            context, MaterialPageRoute(builder: (context) => RecipeDetails(recipeEntry: recipeEntry, image: image)))
        .then((data) => setState(() => {}));
  }
}
