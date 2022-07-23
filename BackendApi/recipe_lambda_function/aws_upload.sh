#!/bin/bash
echo "Uploading to AWS..."

echo "Uploading GET Function"
zip -r zipped_functions/get.zip get_function.py db_connect.py pymysql
aws lambda update-function-code \
    --function-name recipes-get \
    --zip-file fileb://zipped_functions/get.zip

echo "Uploading POST Function"
zip -r zipped_functions/post.zip post_function.py db_connect.py pymysql
aws lambda update-function-code \
    --function-name recipes-post \
    --zip-file fileb://zipped_functions/post.zip

echo "Uploading PUT Function"
zip -r zipped_functions/put.zip put_function.py db_connect.py pymysql
aws lambda update-function-code \
    --function-name recipes-put \
    --zip-file fileb://zipped_functions/put.zip

echo "Uploading DELETE Function"
zip -r zipped_functions/delete.zip delete_function.py db_connect.py pymysql
aws lambda update-function-code \
    --function-name recipes-delete \
    --zip-file fileb://zipped_functions/delete.zip

echo "...Successfully Uploaded to AWS"