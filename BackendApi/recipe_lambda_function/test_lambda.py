from turtle import position
import unittest
import json

from get_function import lambda_handler as get_lambda
from post_function import lambda_handler as post_lambda
from put_function import lambda_handler as put_lambda
from delete_function import lambda_handler as delete_lambda


class TestLambdaMethods(unittest.TestCase):
    def setUp(self):
        self.json_file = "new_recipe.json"

    """
    GET Endpoint Tests
    """
    def test_get(self):
        res = get_lambda(1, 1)
        self.assertEqual(res['statusCode'], 200)

    def test_get_no_ingredients(self):
        postBody = self.load_json()

        # Remove ingredients prior to POST
        postBody["ingredients"] = []
        
        # POST data
        post_res = post_lambda(postBody, 1)

        get_res = get_lambda(1, 1)

        data = json.loads(post_res['body'])
        delete_lambda({'recipeId': data['recipeId']}, 1)

        self.assertEqual(get_res['statusCode'], 200)

    """
    POST Endpoint Tests
    """
    def test_post(self):
        postBody = self.load_json()

        # POST data
        res = post_lambda(postBody, 1)
        data = self.get_body(res)
        delete_lambda({'recipeId': data['recipeId']}, 1)
        self.assertEqual(res['statusCode'], 200)

    def test_post_duplicate(self):
        postBody = self.load_json()

        # POST data twice
        res1 = post_lambda(postBody, 1)
        res2 = post_lambda(postBody, 1)


        data1 = json.loads(res1['body'])
        delete_lambda({'recipeId': data1['recipeId']}, 1)
        self.assertEqual(res2['statusCode'], 409)

    def test_post_same_name(self):
        postBody = self.load_json()

        # POST data
        res1 = post_lambda(postBody, 1)

        # Change the author prior to posting again
        postBody["author"] = "Fake Name"
        # POST data
        res2 = post_lambda(postBody, 1)


        data = json.loads(res1['body'])
        delete_lambda({'recipeId': data['recipeId']}, 1)
        data = json.loads(res2['body'])
        delete_lambda({'recipeId': data['recipeId']}, 1)

        self.assertEqual(res2['statusCode'], 200)

    def test_post_missing_param(self):
        test_keys = ["recipeName", "instructions", "author", "category", "ingredients"]
        for key in test_keys:
            postBody = self.load_json()
            del postBody[key]

            # POST data
            res = post_lambda(postBody, 1)
            data = json.loads(res['body'])
            delete_lambda({'recipeId': data['recipeId']}, 1)
            if res['statusCode'] != 200:
                self.assertEqual(res['statusCode'], 200)

        self.assertEqual(res['statusCode'], 200)

    """
    PUT Endpoint Tests
    """
    def test_put(self):
        putBody = self.load_json()

        # Add something to the database first
        data = post_lambda(putBody, 1)
        dataBody = self.get_body(data)
        putBody["recipeId"] = dataBody["recipeId"]

        # Change something for PUT
        putBody["category"] = "Sauce"

        # PUT data
        res = put_lambda(putBody, 1)

        data = self.get_body(res)
        
        delete_lambda({'recipeId': data['recipeId']}, 1)
        self.assertEqual(res['statusCode'], 200)

    def test_put_no_recipeId(self):
        putBody = self.load_json()
        
        # Add something to the database first
        data = post_lambda(putBody, 1)
        dataBody = self.get_body(data)

        # Send put without recipeId
        resPut = put_lambda(putBody, 1)

        delete_lambda({'recipeId': dataBody['recipeId']}, 1)
        self.assertEqual(resPut['statusCode'], 400)

    def test_put_missing_params(self):
        putBody = self.load_json()

        # Add something to the database first
        data = post_lambda(putBody, 1)
        dataBody = self.get_body(data)

        test_keys = ["recipeName", "instructions", "author", "category"]
        for key in test_keys:
            putBody = dataBody
            del putBody[key]

            res = put_lambda(putBody, 1)
            if res['statusCode'] != 200:
                delete_lambda({'recipeId': dataBody['recipeId']}, 1)
                self.assertEqual(res['statusCode'], 200)

        delete_lambda({'recipeId': dataBody['recipeId']}, 1)
        self.assertEqual(res['statusCode'], 200)

    def test_put_no_ingredients(self):
        putBody = self.load_json()

        # Add something to the database first
        data = post_lambda(putBody, 1)
        dataBody = self.get_body(data)
        del dataBody["ingredients"]

        # Call lambda funciton
        res = put_lambda(dataBody, 1)
        data = self.get_body(res)
        
        delete_lambda({'recipeId': data['recipeId']}, 1)
        self.assertEqual(res['statusCode'], 200)

    """
    DELETE Endpoint Tests
    """
    def test_delete(self):
        postData = self.load_json()
        postRes = post_lambda(postData, 1)
        data = self.get_body(postRes)
        res = delete_lambda({'recipeId': data['recipeId']}, 1)
        self.assertEqual(res['statusCode'], 200)

    def test_delete_no_id(self):
        res = delete_lambda({}, 1)
        self.assertEqual(res['statusCode'], 400)

    def test_delete_bad_id(self):
        res = delete_lambda({"recipeId": 0}, 1)
        self.assertEqual(res['statusCode'], 204)

    """
    Helper methods
    """
    def load_json(self):
        with open(self.json_file) as f:
            body = json.load(f)
        
        return body

    def get_body(self, data):
        try:
            return json.loads(data['body'])
        except(ValueError):
            print(f"Error updating item in DB, response: {data}")


if __name__ == "__main__":
    unittest.main()
