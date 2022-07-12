import 'dart:typed_data';

import 'package:flutter/material.dart';

import '../recipe.dart';
import '../recipe_details.dart';

class FeedTile extends StatefulWidget {
  final Recipe recipeEntry;
  final Uint8List image;

  const FeedTile({
    Key? key,
    required this.recipeEntry,
    required this.image,
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
    // return ListTile(
    //   title: Text(widget.recipeEntry.recipeName),
    //   leading: Image.memory(widget.image),
    //   onTap: () => pushRecipeDetails(context, widget.recipeEntry, widget.image),
    // );
  }

  void pushRecipeDetails(BuildContext context, recipeEntry, image) {
    Navigator.push(
            context, MaterialPageRoute(builder: (context) => RecipeDetails(recipeEntry: recipeEntry, image: image)))
        .then((data) => setState(() => {}));
  }
}
