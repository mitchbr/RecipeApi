import 'dart:typed_data';

import 'package:flutter/material.dart';

import '../../libraries/recipe.dart';
import '../details_page/recipe_details.dart';

class FeedTile extends StatefulWidget {
  final Recipe recipeEntry;
  final Uint8List image;
  final Future<void> fetchRecipes;

  const FeedTile({
    Key? key,
    required this.recipeEntry,
    required this.image,
    required this.fetchRecipes,
  }) : super(key: key);

  @override
  State<FeedTile> createState() => _FeedTileState();
}

class _FeedTileState extends State<FeedTile> {
  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () => pushRecipeDetails(context, widget.recipeEntry, widget.image),
      child: SingleChildScrollView(
        child: Column(
          children: [
            SizedBox(height: 15),
            Image.memory(
              widget.image,
              width: MediaQuery.of(context).size.width,
            ),
            ListTile(
              title: Text(widget.recipeEntry.recipeName),
              subtitle: Text(widget.recipeEntry.author),
            ),
          ],
        ),
      ),
    );
  }

  void pushRecipeDetails(BuildContext context, recipeEntry, image) {
    Navigator.push(
            context, MaterialPageRoute(builder: (context) => RecipeDetails(recipeEntry: recipeEntry, image: image)))
        .then((data) => setState(() => {widget.fetchRecipes}));
  }
}
