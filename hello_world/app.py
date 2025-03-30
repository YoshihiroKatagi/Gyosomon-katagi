import os
import boto3
import json
import uuid

# DynamoDB へ接続
dynamodb = boto3.resource("dynamodb", endpoint_url=os.getenv("DYNAMODB_ENDPOINT"))
table = dynamodb.Table("SampleTable")  # DynamoDB のテーブル名を 'SampleTable' に変更

def lambda_handler(event, context):
    # "Id" が "123" のアイテムを取得
    response = table.get_item(
        Key={
            'Id': '123'
        }
    )

    # データが存在する場合
    if 'Item' in response:
        item = response['Item']
        return {
            "statusCode": 200,
            "body": json.dumps(item)
        }
    else:
        # データが見つからなかった場合
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Item not found"})
        }

# def lambda_handler(event, context):
#     # データを DynamoDB に保存
#     item = {
#         "Id": str(uuid.uuid4()),  # 'id' を 'Id' に変更（テーブル定義に合わせる）
#         "Message": "Hello, AWS SAM!"  # 'message' を 'Message' に変更（テーブル定義に合わせる）
#     }
#     table.put_item(Item=item)

#     return {
#         "statusCode": 200,
#         "body": json.dumps(item)
#     }


# import json

# # import requests


# def lambda_handler(event, context):
#     """Sample pure Lambda function

#     Parameters
#     ----------
#     event: dict, required
#         API Gateway Lambda Proxy Input Format

#         Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

#     context: object, required
#         Lambda Context runtime methods and attributes

#         Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

#     Returns
#     ------
#     API Gateway Lambda Proxy Output Format: dict

#         Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
#     """

#     # try:
#     #     ip = requests.get("http://checkip.amazonaws.com/")
#     # except requests.RequestException as e:
#     #     # Send some context about this error to Lambda Logs
#     #     print(e)

#     #     raise e

#     return {
#         "statusCode": 200,
#         "body": json.dumps({
#             "message": "hello world",
#             # "location": ip.text.replace("\n", "")
#         }),
#     }
