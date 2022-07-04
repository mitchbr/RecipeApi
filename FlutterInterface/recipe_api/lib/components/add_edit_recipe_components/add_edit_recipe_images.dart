import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';

import 'add_edit_recipe_ingredients.dart';
import '../recipe.dart';

class AddEditRecipeImages extends StatefulWidget {
  final Recipe recipeMetadata;
  final String tag;
  // TODO: Display old image, only push image if it's updated
  final Uint8List? recipeImage;
  const AddEditRecipeImages({Key? key, required this.recipeMetadata, required this.tag, this.recipeImage})
      : super(key: key);

  @override
  State<AddEditRecipeImages> createState() => _AddEditRecipeImagesState();
}

class _AddEditRecipeImagesState extends State<AddEditRecipeImages> {
  File? image;
  late XFile imagePath;

  late String tag;
  late Recipe entryData;

  @override
  void initState() {
    tag = widget.tag;
    if (tag == "Edit") {
      var im = Image.memory(widget.recipeImage!);
      image = File(im.toString());
    }
    entryData = widget.recipeMetadata;
    super.initState();
  }

  Future pickImageGallery() async {
    try {
      imagePath = (await ImagePicker().pickImage(source: ImageSource.gallery))!;

      if (imagePath == null) return;

      final imageFile = File(imagePath.path);
      setState(() => image = imageFile);
    } on PlatformException {
      return;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(" Recipe"),
      ),
      body: formContent(context),
    );
  }

  Widget formContent(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Center(
          child: Column(children: [
        image != null
            ? SizedBox(
                child: Image.file(image!),
                height: 400, // TODO: Adjust this image height value
              )
            : ElevatedButton(child: const Text('Choose from Gallery'), onPressed: () => pickImageGallery()),
        const SizedBox(height: 20),
        image != null
            ? ElevatedButton(
                child: const Text('Change Image'),
                onPressed: () => pickImageGallery(),
              )
            : SizedBox(height: 2),
        const SizedBox(height: 20),
        image != null ? nextButton(context) : SizedBox(height: 0),
      ])),
    );
  }

  /*
   *
   * Push next page
   * 
   */
  Widget nextButton(BuildContext context) {
    return ElevatedButton(
        onPressed: () async {
          addImageToRecipe();
          pushAddEditRecipePreview(context);
        },
        child: const Text('Next'));
  }

  void addImageToRecipe() {
    entryData.images.add(imagePath.path);
  }

  void pushAddEditRecipePreview(BuildContext context) {
    Navigator.push(context,
            MaterialPageRoute(builder: (context) => AddEditRecipeIngredients(recipeMetadata: entryData, tag: tag)))
        .then((data) => setState(() => {}));
  }
}
