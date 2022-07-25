#!/bin/bash
echo "Uploading to AWS..."
ls

echo "Uploading GET Function"
zip -r zipped_functions/author-get.zip authors_lambdas/author_get.py database
aws lambda update-function-code \
    --function-name author-get \
    --zip-file fileb://zipped_functions/author-get.zip

echo "Uploading POST Function"
zip -r zipped_functions/author-post.zip authors_lambdas/author_post.py database
aws lambda update-function-code \
    --function-name author-post \
    --zip-file fileb://zipped_functions/author-post.zip

echo "Uploading PUT Function"
zip -r zipped_functions/author-put.zip authors_lambdas/author_put.py database
aws lambda update-function-code \
    --function-name author-put \
    --zip-file fileb://zipped_functions/author-put.zip

echo "Uploading DELETE Function"
zip -r zipped_functions/author-delete.zip authors_lambdas/author_delete.py database
aws lambda update-function-code \
    --function-name author-delete \
    --zip-file fileb://zipped_functions/author-delete.zip

echo "...Done"