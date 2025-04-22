#!/bin/sh

# DynamoDB Local にテーブル作成
aws dynamodb create-table \
    --table-name SampleTable \
    --attribute-definitions AttributeName=Id,AttributeType=S \
    --key-schema AttributeName=Id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --endpoint-url http://localhost:8000 \
    --region ap-northeast-1

# データ挿入
aws dynamodb put-item \
    --table-name SampleTable \
    --item '{"Id": {"S": "123"}, "Message": {"S": "Hello, World!"}}' \
    --endpoint-url http://localhost:8000 \
    --region ap-northeast-1

echo "DynamoDB table and initial data created."

# データ確認
aws dynamodb query --table-name SampleTable --key-condition-expression "Id = :id" --expression-attribute-values '{":id": {"S": "123"}}' --endpoint-url http://localhost:8000 --region ap-northeast-1
