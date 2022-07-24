#!/bin/bash
echo "Uploading to AWS..."

echo "Uploading GET Function"
zip -r zipped_functions/ingredients-get.zip /ingredients_lambdas/ingredients_get.py database
aws lambda update-function-code \
    --function-name ingredients-get \
    --zip-file fileb://zipped_functions/ingredients-get.zip

echo "...Done"