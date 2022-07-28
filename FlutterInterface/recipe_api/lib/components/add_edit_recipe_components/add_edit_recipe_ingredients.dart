import 'dart:typed_data';

import 'package:flutter/material.dart';

import '../../types/recipe.dart';
import 'package:recipe_api/components/add_edit_recipe_components/add_edit_recipe_preview.dart';

class AddEditRecipeIngredients extends StatefulWidget {
  final Recipe recipeMetadata;
  final String tag;
  final Uint8List? recipeImage;
  const AddEditRecipeIngredients({Key? key, required this.recipeMetadata, required this.tag, required this.recipeImage})
      : super(key: key);

  @override
  State<AddEditRecipeIngredients> createState() => _AddEditRecipeIngredientsState();
}

class _AddEditRecipeIngredientsState extends State<AddEditRecipeIngredients> {
  final formKey = GlobalKey<FormState>();
  late Map<String, dynamic> currentIngredient = {};
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _amountController = TextEditingController();
  final TextEditingController _unitController = TextEditingController();

  late String tag;
  late Recipe entryData;

  @override
  void initState() {
    tag = widget.tag;
    entryData = widget.recipeMetadata;
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("$tag Recipe"),
      ),
      body: formContent(context),
    );
  }

  /*
   *
   * Ingredient Form layout
   * 
   */
  Widget formContent(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.all(20),
        child: ListView.builder(
            itemCount: entryData.ingredients.length + 2,
            itemBuilder: (context, index) {
              if (index == 0) {
                return const ListTile(
                    title: Text(
                  'Ingredients',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ));
              } else if (index == entryData.ingredients.length + 1) {
                return Column(
                  children: [
                    newEntryBox(),
                    const SizedBox(height: 10),
                    nextButton(context),
                  ],
                );
              } else {
                return ingredientTile(index - 1);
              }
            }));
  }

  /*
   *
   * New ingredient forms
   * 
   */
  Widget newEntryBox() {
    return Form(
        key: formKey,
        child: ListTile(
          title: Row(
            children: <Widget>[
              Expanded(child: ingredientNameField()),
              Expanded(child: ingredientAmountField()),
              Expanded(child: ingredientUnitField()),
            ],
          ),
          trailing: IconButton(onPressed: (() => saveIngredient()), icon: const Icon(Icons.add)),
        ));
  }

  Widget ingredientNameField() {
    return TextFormField(
      controller: _nameController,
      autofocus: true,
      decoration: const InputDecoration(labelText: 'Name', border: OutlineInputBorder()),
      textCapitalization: TextCapitalization.words,
      onSaved: (value) {
        if (value != null) {
          currentIngredient['ingredientName'] = value;
        }
      },
      validator: (value) {
        var val = value;
        if (val != null) {
          if (val.isEmpty) {
            return 'Please enter a value';
          } else {
            return null;
          }
        }
      },
    );
  }

  Widget ingredientAmountField() {
    return TextFormField(
      controller: _amountController,
      autofocus: true,
      decoration: const InputDecoration(labelText: 'Amount', border: OutlineInputBorder()),
      textCapitalization: TextCapitalization.words,
      onSaved: (value) {
        if (value != null) {
          currentIngredient['ingredientAmount'] = value;
        }
      },
      validator: (value) {
        var val = value;
        if (val != null) {
          if (val.isEmpty) {
            return 'Please enter a value';
          } else {
            return null;
          }
        }
      },
    );
  }

  Widget ingredientUnitField() {
    return TextFormField(
      controller: _unitController,
      autofocus: true,
      decoration: const InputDecoration(labelText: 'Unit', border: OutlineInputBorder()),
      textCapitalization: TextCapitalization.words,
      onSaved: (value) {
        if (value != null) {
          currentIngredient['ingredientUnit'] = value;
        }
      },
      validator: (value) {
        var val = value;
        if (val != null) {
          if (val.isEmpty) {
            return 'Please enter a value';
          } else {
            return null;
          }
        }
      },
    );
  }

  void saveIngredient() {
    var currState = formKey.currentState;
    if (currState != null) {
      if (currState.validate()) {
        currState.save();

        setState(() {
          entryData.ingredients.add(currentIngredient);
          currentIngredient = {};
          _nameController.clear();
          _amountController.clear();
          _unitController.clear();
        });
      }
    }
  }

  /*
   *
   * Ingredient display tile
   * 
   */
  Widget ingredientTile(int index) {
    return ListTile(
      title: Text('${entryData.ingredients[index]['ingredientName']} '
          '(${entryData.ingredients[index]['ingredientAmount']} '
          '${entryData.ingredients[index]['ingredientUnit']})'),
      trailing: IconButton(onPressed: (() => removeIngredient(index)), icon: const Icon(Icons.close)),
    );
  }

  void removeIngredient(int index) {
    setState(() {
      entryData.ingredients.removeAt(index);
    });
  }

  /*
   *
   * Push next page
   * 
   */
  Widget nextButton(BuildContext context) {
    return TextButton(
        style: TextButton.styleFrom(
          padding: const EdgeInsets.all(16.0),
          primary: Colors.white,
          textStyle: const TextStyle(fontSize: 20),
          backgroundColor: Colors.purple, // TODO: Make this auto-update with style
        ),
        onPressed: () async {
          pushAddEditRecipePreview(context);
        },
        child: const Text('Next'));
  }

  void pushAddEditRecipePreview(BuildContext context) {
    Navigator.push(
        context,
        MaterialPageRoute(
            builder: (context) => AddEditRecipePreview(
                  recipeMetadata: entryData,
                  tag: tag,
                  recipeImage: widget.recipeImage,
                ))).then((data) => setState(() => {}));
  }
}
