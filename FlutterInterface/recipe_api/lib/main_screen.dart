import 'package:flutter/material.dart';

import 'components/recipes_feed.dart';

class Groceries extends StatefulWidget {
  const Groceries({Key? key}) : super(key: key);

  @override
  _GroceriesState createState() => _GroceriesState();
}

class _GroceriesState extends State<Groceries> {
  _GroceriesState();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'Recipes',
        theme: ThemeData(colorScheme: const ColorScheme.dark()),
        home: DefaultTabController(length: 2, child: Builder(builder: (context) => groceriesScaffold(context))));
  }

  Widget groceriesScaffold(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Recipe Api"),
      ),
      body: const RecipesView(),
    );
  }
}
