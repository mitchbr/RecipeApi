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
  final Uint8List? recipeImage;
  const AddEditRecipeImages({Key? key, required this.recipeMetadata, required this.tag, this.recipeImage})
      : super(key: key);

  @override
  State<AddEditRecipeImages> createState() => _AddEditRecipeImagesState();
}

class _AddEditRecipeImagesState extends State<AddEditRecipeImages> {
  Image? image;
  late XFile imagePath;
  late Uint8List recipeImage;
  late Uint8List imageFile;

  late String tag;
  late Recipe entryData;

  @override
  void initState() {
    tag = widget.tag;
    if (tag == "Edit") {
      image = Image.memory(widget.recipeImage!);
    }
    entryData = widget.recipeMetadata;
    super.initState();
  }

  Future pickImageGallery() async {
    try {
      imagePath = (await ImagePicker().pickImage(source: ImageSource.gallery))!;

      if (imagePath == null) return;

      imageFile = await File(imagePath.path).readAsBytes();
      setState(() => image = Image.memory(imageFile));
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
      child: SingleChildScrollView(
          child: Column(children: [
        image != null
            ? SizedBox(
                child: image,
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
    // entryData.images.add(imagePath.path);
    if (tag == 'Edit') {
      recipeImage = widget.recipeImage!;
    } else {
      recipeImage = imageFile;
    }
  }

  void pushAddEditRecipePreview(BuildContext context) {
    Navigator.push(
            context,
            MaterialPageRoute(
                builder: (context) =>
                    AddEditRecipeIngredients(recipeMetadata: entryData, tag: tag, recipeImage: recipeImage)))
        .then((data) => setState(() => {}));
  }
}
