from utils import (
    get_table_prefix,
    get_dynamodb_resource
)
import os
import boto3
import json
import uuid
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB へ接続
# dynamodb = boto3.resource("dynamodb", endpoint_url=os.getenv("DYNAMODB_ENDPOINT"))
dynamodb = boto3.resource('dynamodb', endpoint_url="http://host.docker.internal:8000")
table = dynamodb.Table("SampleTable")

def lambda_handler(event, context):
    # results = {"message": "Test, SampleFanction"}
    results = {}

    prefix = get_table_prefix(event)
    # stage_variables = event.get('stageVariables') or {}
    # logger.info(f"stage_variables: {stage_variables}")
    # alias = stage_variables.get('alias', '')
    # logger.info(f"alias: {alias}")

    dynamodb = get_dynamodb_resource(event)
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://host.docker.internal:8000")

    # ① レコード追加
    new_item = {
        "Id": str(uuid.uuid4()),
        "Message": "Hello, AWS SAM!"
    }
    table.put_item(Item=new_item)
    results["PutItem"] = new_item

    # ② テーブル全件取得（一覧）
    scan_response = table.scan()
    all_items = scan_response.get("Items", [])
    results["Scan"] = all_items

    # ③ ID = "123" のアイテムを検索
    get_response = table.get_item(Key={"Id": "123"})
    if "Item" in get_response:
        results["GetItem"] = get_response["Item"]
    else:
        results["GetItem"] = "Item with Id=123 not found"

    # ④ 追加したレコードを削除
    table.delete_item(Key={"Id": new_item["Id"]})
    results["DeleteItem"] = f"Deleted Id={new_item['Id']}"

    return {
        "statusCode": 200,
        "body": json.dumps(results, indent=2)
    }