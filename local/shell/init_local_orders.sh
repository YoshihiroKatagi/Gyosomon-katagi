#!/bin/sh

# DynamoDB Local にテーブル作成（/local/tables/definition/ 下のJSONファイル参照）
aws dynamodb create-table \
    --cli-input-json file://../tables/definition/local_orders.json \
    --endpoint-url http://localhost:8000 \
    --region ap-northeast-1

# データ挿入（/local/tables/data/ 下のJSONファイル参照）
aws dynamodb put-item \
    --table-name local_orders \
    --item file://../tables/data/local_orders.json \
    --endpoint-url http://localhost:8000 \
    --region ap-northeast-1

echo "local_orders table and initial data created."

# データ確認
aws dynamodb scan \
    --table-name local_orders \
    --endpoint-url http://localhost:8000 \
    --region ap-northeast-1

# aws dynamodb query \
#     --table-name local_orders \
#     --key-condition-expression "order_id = :order_id" \
#     --expression-attribute-values '{":order_id": {"S": "2501300002"}}' \
#     --endpoint-url http://localhost:8000 \
#     --region ap-northeast-1
