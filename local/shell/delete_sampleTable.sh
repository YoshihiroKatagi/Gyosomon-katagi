#!/bin/sh

# テーブル削除
aws dynamodb delete-table \
    --table-name SampleTable \
    --endpoint-url http://localhost:8000 \
    --region ap-northeast-1

echo "DynamoDB table and data deleted."