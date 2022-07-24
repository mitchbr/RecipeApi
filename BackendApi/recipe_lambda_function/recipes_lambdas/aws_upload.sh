#!/bin/bash
echo "Uploading to AWS..."

echo "Uploading GET Function"
zip -r zipped_functions/recipes-get.zip recipes_get.py $PWD/../database/db_connect.py $PWD/../database/pymysql
aws lambda update-function-code \
    --function-name recipes-get \
    --zip-file fileb://zipped_functions/recipes-get.zip

echo "Uploading POST Function"
zip -r zipped_functions/recipes-post.zip recipes_post.py $PWD/../database/db_connect.py $PWD/../database/pymysql
aws lambda update-function-code \
    --function-name recipes-post \
    --zip-file fileb://zipped_functions/recipes-post.zip

echo "Uploading PUT Function"
zip -r zipped_functions/recipes-put.zip recipes_put.py $PWD/../database/db_connect.py $PWD/../database/pymysql
aws lambda update-function-code \
    --function-name recipes-put \
    --zip-file fileb://zipped_functions/recipes-put.zip

echo "Uploading DELETE Function"
zip -r zipped_functions/recipes-delete.zip recipes_delete.py $PWD/../database/db_connect.py $PWD/../database/pymysql
aws lambda update-function-code \
    --function-name recipes-delete \
    --zip-file fileb://zipped_functions/recipes-delete.zip

echo "...Successfully Uploaded to AWS"