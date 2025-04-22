import boto3
import logging
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_alias(event):
    # eventからstageVariablesを取得
    stage_variables = event.get('stageVariables') or {}
    alias = stage_variables.get('alias') or 'local'
    logger.info(f"stage_variables: {stage_variables}")
    logger.info(f"alias: {alias}")
    return alias

def get_table_prefix(event):
    alias = get_alias(event)
    if alias == 'prod':
        return ''
    # else:
    #     return 'dev_'
    elif alias == 'dev':
        return 'dev_'
    else:
        return 'local_'

def get_dynamodb_resource(event):
    alias = get_alias(event)

    # ローカル環境ではendpoint_urlを指定
    if alias == 'local':
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://host.docker.internal:8000")  # ローカルDynamoDB
    else:
        dynamodb = boto3.resource('dynamodb')  # dev、prodではAWSのDynamoDBを使用
    
    return dynamodb

def send_email(recipients, subject, body):
    client = boto3.client('ses', region_name="ap-northeast-1")
    sender = "八葉水産 <no-reply@shachi-order.com>"
    try:
        response = client.send_email(
            Destination={'ToAddresses': recipients},
            Message={
                'Body': {'Text': {'Charset': "UTF-8", 'Data': body}},
                'Subject': {'Charset': "UTF-8", 'Data': subject},
            },
            Source=sender
        )
        return response
    except ClientError as e:
        logger.error(f"Email send failed: {e.response['Error']['Message']}")
        raise


# # todo: 今後のlayer化で使用可能
# def get_dynamodb_table(prefix, table_name):
#     return dynamodb.Table(prefix + table_name)

# # todo: 今後のlayer化で使用可能
# def get_item_by_key(table, key):
#     try:
#         response = table.get_item(Key=key)
#         return response.get("Item", {})
#     except Exception as err:
#         logger.error(f"Error fetching item from {table.table_name}: {err}")
#         raise
# # todo: 今後のlayer化で使用可能
# def update_item_status(table, key, update_expr, expr_values):
#     try:
#         response = table.update_item(
#             Key=key,
#             UpdateExpression=update_expr,
#             ExpressionAttributeValues=expr_values,
#             ReturnValues='UPDATED_NEW'
#         )
#         return response
#     except Exception as err:
#         logger.error(f"Error updating item in {table.table_name}: {err}")
#         raise

# # todo: 今後のlayer化で使用可能
# def get_current_time_jst():
#     utc_now = datetime.utcnow()
#     return (utc_now + timedelta(hours=9)).isoformat()
