#!/bin/bash
echo "Uploading to AWS..."
ls

echo "Uploading GET Function"
zip -r zipped_functions/author-get.zip authors_lambdas/author_get.py database
aws lambda update-function-code \
    --function-name author-get \
    --zip-file fileb://zipped_functions/author-get.zip

echo "...Done"