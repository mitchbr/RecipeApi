import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'package:flutter/services.dart';

import '../recipe.dart';

class AddEditRecipePreview extends StatefulWidget {
  final Recipe recipeMetadata;
  final String tag;
  final Uint8List? recipeImage;
  const AddEditRecipePreview({Key? key, required this.recipeMetadata, required this.tag, required this.recipeImage})
      : super(key: key);

  @override
  State<AddEditRecipePreview> createState() => _AddEditRecipePreviewState();
}

class _AddEditRecipePreviewState extends State<AddEditRecipePreview> {
  Image? image;
  late String tag;
  late Recipe entryData;

  @override
  void initState() {
    tag = widget.tag;
    image = Image.memory(widget.recipeImage!);
    entryData = widget.recipeMetadata;
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("$tag Recipe"),
      ),
      body: bodyContent(context),
    );
  }

  /*
   *
   * Main list content
   * 
   */
  Widget bodyContent(BuildContext context) {
    return ListView.builder(
      itemCount: entryData.ingredients.length + 2,
      itemBuilder: (context, index) {
        if (index == 0) {
          return recipeMetaData();
        } else if (index == entryData.ingredients.length + 1) {
          return Column(
            children: [recipeDetails(), const SizedBox(height: 10), publishButton(context)],
          );
        } else {
          return ingredientTile(index - 1);
        }
      },
    );
  }

  /*
   *
   * List Tiles
   * 
   */
  Widget recipeMetaData() {
    return Column(
      children: [
        SizedBox(
          child: image,
          height: 400,
        ),
        ListTile(
            title: Text(
          entryData.recipeName,
          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        )),
        const ListTile(
            title: Text(
          'Ingredients',
          style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        )),
      ],
    );
  }

  Widget recipeDetails() {
    return Column(children: [
      const ListTile(
          title: Text(
        'Instructions',
        style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
      )),
      ListTile(title: Text(entryData.instructions)),
      const ListTile(
          title: Text(
        'Details',
        style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
      )),
      ListTile(title: Text('Author: ${entryData.author}')),
      ListTile(title: Text('Category: ${entryData.category}')),
    ]);
  }

  Widget ingredientTile(int index) {
    return ListTile(
      title: Text('${entryData.ingredients[index]['ingredientName']} '
          '(${entryData.ingredients[index]['ingredientAmount']} '
          '${entryData.ingredients[index]['ingredientUnit']})'),
    );
  }

  /*
   *
   * Publish Recipe
   * 
   */
  Widget publishButton(BuildContext context) {
    return TextButton(
        style: TextButton.styleFrom(
          padding: const EdgeInsets.all(16.0),
          primary: Colors.white,
          textStyle: const TextStyle(fontSize: 20),
          backgroundColor: Colors.purple, // TODO: Make this auto-update with style
        ),
        onPressed: () async {
          final httpBody = entryData.toJson();
          final String jsonData = await rootBundle.loadString('assets/api_url.json');
          final apiUrl = await json.decode(jsonData);
          if (tag == 'Add') {
            // Create Recipe
            await http.post(Uri.parse('${apiUrl['url']}/recipes'),
                headers: <String, String>{
                  'Content-Type': 'application/json; charset=UTF-8',
                },
                body: jsonEncode(httpBody));
          } else {
            // Update Recipe
            http.put(Uri.parse('${apiUrl['url']}/recipes'),
                headers: <String, String>{
                  'Content-Type': 'application/json; charset=UTF-8',
                },
                body: jsonEncode(httpBody));
          }
          uploadImage(apiUrl);

          Navigator.of(context).popUntil((route) => route.isFirst);
        },
        child: const Text('Publish'));
  }

  void uploadImage(apiUrl) async {
    final imageName = "${entryData.recipeName}_${entryData.author}.jpeg";
    var client = http.Client();
    var request = http.Request(
        'PUT',
        // TODO: Convert to URL variable
        Uri.parse(
            'https://0rbzt2fsha.execute-api.us-east-2.amazonaws.com/dev/images/mitchell-recipe-images/$imageName'));
    request.headers.addAll({'Content-Type': 'image/jpeg'});
    request.bodyBytes = widget.recipeImage!;
    var streamedResponse = await client.send(request).then((res) {
      print("image upload response: ${res.statusCode}");
    }).catchError((err) {
      print(err);
    });
    client.close();
  }
}
