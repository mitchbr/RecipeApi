from turtle import position
import unittest
import json

from lambda_function import lambda_handler


class TestLambdaMethods(unittest.TestCase):
    def setUp(self):
        self.GET_RAW_PATH = "/getRecipes"
        self.CREATE_RAW_PATH = "/createRecipe"
        self.PUT_RAW_PATH = "/updateRecipe"
        self.DELETE_RAW_PATH = "/deleteRecipe"
        self.jsonFile = "postRecipe.json"

    """
    GET Endpoint Tests
    """
    def test_get(self):
        res = self.call_lambda_handler(self.GET_RAW_PATH, "")
        self.assertEqual(res['statusCode'], 200)

    def test_get_no_ingredients(self):
        postBody = self.load_json()

        # Remove ingredients prior to POST
        postBody["ingredients"] = []
        
        # POST data
        post_res = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(postBody))

        get_res = self.call_lambda_handler(self.GET_RAW_PATH, "")

        data = json.loads(post_res['body'])
        self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': data['recipeId']}))

        self.assertEqual(get_res['statusCode'], 200)

    def test_get_no_images(self):
        postBody = self.load_json()

        # Remove ingredients prior to POST
        postBody["images"] = []

        # POST data
        post_res = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(postBody))

        get_res = self.call_lambda_handler(self.GET_RAW_PATH, "")

        data = json.loads(post_res['body'])
        self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': data['recipeId']}))

        self.assertEqual(get_res['statusCode'], 200)

    """
    POST Endpoint Tests
    """
    def test_post(self):
        postBody = self.load_json()

        # POST data
        res = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(postBody))
        data = self.get_body(res)
        self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': data['recipeId']}))
        self.assertEqual(res['statusCode'], 200)

    def test_post_duplicate(self):
        postBody = self.load_json()

        # POST data twice
        res1 = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(postBody))
        res2 = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(postBody))


        data1 = json.loads(res1['body'])
        self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': data1['recipeId']}))
        self.assertEqual(res2['statusCode'], 409)

    def test_post_same_name(self):
        postBody = self.load_json()

        # POST data
        res1 = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(postBody))

        # Change the author prior to posting again
        postBody["author"] = "Fake Name"
        # POST data
        res2 = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(postBody))


        data = json.loads(res1['body'])
        self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': data['recipeId']}))
        data = json.loads(res2['body'])
        self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': data['recipeId']}))

        self.assertEqual(res2['statusCode'], 200)

    def test_post_missing_param(self):
        test_keys = ["recipeName", "instructions", "author", "category", "ingredients", "images"]
        for key in test_keys:
            postBody = self.load_json()
            del postBody[key]

            # POST data
            res = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(postBody))
            data = json.loads(res['body'])
            self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': data['recipeId']}))
            if res['statusCode'] != 200:
                self.assertEqual(res['statusCode'], 200)

        self.assertEqual(res['statusCode'], 200)

    """
    PUT Endpoint Tests
    """
    def test_put(self):
        putBody = self.load_json()

        # Add something to the database first
        data = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(putBody))
        dataBody = self.get_body(data)
        putBody["recipeId"] = dataBody["recipeId"]

        # Change something for PUT
        putBody["category"] = "Sauce"

        # PUT data
        res = self.call_lambda_handler(self.PUT_RAW_PATH, json.dumps(putBody))

        data = self.get_body(res)
        
        self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': data['recipeId']}))
        self.assertEqual(res['statusCode'], 200)

    def test_put_no_recipeId(self):
        putBody = self.load_json()
        
        # Add something to the database first
        data = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(putBody))
        dataBody = self.get_body(data)

        # Send put without recipeId
        resPut = self.call_lambda_handler(self.PUT_RAW_PATH, json.dumps(putBody))

        self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': dataBody['recipeId']}))
        self.assertEqual(resPut['statusCode'], 400)

    def test_put_missing_params(self):
        putBody = self.load_json()

        # Add something to the database first
        data = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(putBody))
        dataBody = self.get_body(data)

        test_keys = ["recipeName", "instructions", "author", "category"]
        for key in test_keys:
            putBody = dataBody
            del putBody[key]

            res = self.call_lambda_handler(self.PUT_RAW_PATH, json.dumps(putBody))
            if res['statusCode'] != 200:
                self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': dataBody['recipeId']}))
                self.assertEqual(res['statusCode'], 200)

        self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': dataBody['recipeId']}))
        self.assertEqual(res['statusCode'], 200)

    def test_put_no_ingredients(self):
        putBody = self.load_json()

        # Add something to the database first
        data = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(putBody))
        dataBody = self.get_body(data)
        del dataBody["ingredients"]

        # Set up lambda inputs
        event = {"rawPath": self.PUT_RAW_PATH, "body": json.dumps(dataBody)}
        context = 1

        # Call lambda funciton
        res = lambda_handler(event, context)
        data = self.get_body(res)
        
        self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': data['recipeId']}))
        self.assertEqual(res['statusCode'], 200)

    def test_put_no_images(self):
        putBody = self.load_json()

        # Add something to the database first
        data = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(putBody))
        dataBody = self.get_body(data)
        del dataBody["images"]

        # Set up lambda inputs
        event = {"rawPath": self.PUT_RAW_PATH, "body": json.dumps(dataBody)}
        context = 1

        # Call lambda funciton
        res = lambda_handler(event, context)
        data = self.get_body(res)
        self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': dataBody['recipeId']}))
        self.assertEqual(res['statusCode'], 200)


    """
    DELETE Endpoint Tests
    """
    def test_delete(self):
        postData = self.load_json()
        postRes = self.call_lambda_handler(self.CREATE_RAW_PATH, json.dumps(postData))
        data = self.get_body(postRes)
        res = self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({'recipeId': data['recipeId']}))
        self.assertEqual(res['statusCode'], 200)

    def test_delete_no_id(self):
        res = self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({}))
        self.assertEqual(res['statusCode'], 400)

    def test_delete_bad_id(self):
        res = self.call_lambda_handler(self.DELETE_RAW_PATH, json.dumps({"recipeId": 0}))
        self.assertEqual(res['statusCode'], 204)

    """
    Helper methods
    """
    def load_json(self):
        with open(self.jsonFile) as f:
            body = json.load(f)
        
        return body

    def call_lambda_handler(self, path, body):
        # Set up lambda inputs
        event = {"rawPath": path, "body": body}
        context = 1

        return lambda_handler(event, context)

    def get_body(self, data):
        try:
            return json.loads(data['body'])
        except(ValueError):
            print(f"Error updating item in DB, response: {data}")


if __name__ == "__main__":
    unittest.main()
