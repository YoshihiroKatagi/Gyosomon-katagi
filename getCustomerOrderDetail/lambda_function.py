from utils import (
    get_table_prefix,
    get_dynamodb_resource
)
import boto3
import json 
from decimal import Decimal
# import os
# dynamodb_endpoint = os.getenv("DYNAMODB_ENDPOINT", None)
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # alias=prodの場合:prefix='',  alias=devの場合:prefix='dev_'
        prefix = get_table_prefix(event)
        dynamodb = get_dynamodb_resource(event)
        # dynamodb = boto3.resource('dynamodb', endpoint_url="http://host.docker.internal:8000")

        # テーブル名取得
        orders_table_name = prefix + 'orders'
        logger.info(f"Using DynamoDB TableName: {orders_table_name}")

        customer_id = get_customer_id(event)
        order_id = get_order_id(event)
        
        order_info = get_order_info(customer_id, order_id, orders_table_name, dynamodb)
        logger.info(f"customer_id: {customer_id}")
        logger.info(f"order_id: {order_id}")
        
        return {
            'statusCode': 200,
            'headers':{
                'Access-Control-Allow-Origin':'*'
            },
            'body': json.dumps(order_info, default=decimal_to_int, ensure_ascii=False)
        }
    except Exception as e:
        body = 'message:{}'.format(e)
        return{
            'statusCode': 500,
            'headers':{
                'Access-Control-Allow-Origin':'*'
            },
            'body': json.dumps(body, ensure_ascii=False)
        }



def get_customer_id(event):
    try:
        id = event['queryStringParameters']['customer_id']

        return id
    except Exception as e:
        raise Exception('Failed to get customer_id. error:{}'.format(e))



def get_order_id(event):
    try:
        id = event['queryStringParameters']['order_id']

        return id
    except Exception as e:
        raise Exception('Failed to get order_id. error:{}'.format(e))



def get_order_info(customer_id, order_id, orders_table_name, dynamodb):
    try:
        orders_table = dynamodb.Table(orders_table_name)
        response = orders_table.get_item(
            Key={
                'order_id': order_id
            }
        )
        
        order_info = response["Item"]
        
        if order_info["customer_id"] == customer_id:
            return order_info
        else:
            raise Exception('This order info is not yours')
        
    except Exception as err:
        print("Error occurred while fetching order info:", err)
        return ""

        
        

def decimal_to_int(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    elif isinstace(obj, Int):
        return obj
    else:
        raise Exception