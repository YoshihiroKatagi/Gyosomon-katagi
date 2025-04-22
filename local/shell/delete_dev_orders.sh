#!/bin/sh

# テーブル削除
aws dynamodb delete-table \
    --table-name dev_orders \
    --endpoint-url http://localhost:8000 \
    --region ap-northeast-1

echo "local tables and data deleted."