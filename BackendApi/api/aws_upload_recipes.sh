#!/bin/bash
echo "Uploading to AWS..."

echo "Uploading GET Function"
zip -r zipped_functions/recipes-get.zip recipes_lambdas/recipes_get.py database
aws lambda update-function-code \
    --function-name recipes-get \
    --zip-file fileb://zipped_functions/recipes-get.zip

echo "Uploading POST Function"
zip -r zipped_functions/recipes-post.zip recipes_lambdas/recipes_post.py database
aws lambda update-function-code \
    --function-name recipes-post \
    --zip-file fileb://zipped_functions/recipes-post.zip

echo "Uploading PUT Function"
zip -r zipped_functions/recipes-put.zip recipes_lambdas/recipes_put.py database
aws lambda update-function-code \
    --function-name recipes-put \
    --zip-file fileb://zipped_functions/recipes-put.zip

echo "Uploading DELETE Function"
zip -r zipped_functions/recipes-delete.zip recipes_lambdas/recipes_delete.py database
aws lambda update-function-code \
    --function-name recipes-delete \
    --zip-file fileb://zipped_functions/recipes-delete.zip

echo "...Successfully Uploaded to AWS"