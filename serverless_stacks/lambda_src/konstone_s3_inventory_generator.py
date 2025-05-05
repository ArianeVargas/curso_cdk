# lambda/handler.py
import boto3
import json
import logging
import os

s3_client = boto3.client('s3')
ddb = boto3.resource('dynamodb')

logger = logging.getLogger()
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO').upper())

def ddb_put_item(item):
    """Insert item into DynamoDB table"""
    table_name = os.environ.get('DDB_TABLE_NAME')
    if not table_name:
        raise ValueError("Environment variable DDB_TABLE_NAME not set")
    
    table = ddb.Table(table_name)
    try:
        table.put_item(Item=item)
    except Exception as e:
        logger.error(f"Error inserting item into DynamoDB: {e}")
        raise

def get_buckets_inventory():
    """Generate list of S3 buckets"""
    try:
        resp = s3_client.list_buckets()
        inventory = {"buckets": []}
        for bucket in resp.get('Buckets', []):
            name = bucket["Name"]
            inventory["buckets"].append(name)
            ddb_put_item({"_id": name})
        return inventory
    except Exception as e:
        logger.error(f"Error fetching bucket inventory: {e}")
        raise

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    response = {
        "statusCode": 400,
        "body": json.dumps({"message": "Error processing request."})
    }

    try:
        inventory = get_buckets_inventory()
        response["statusCode"] = 200
        response["body"] = json.dumps({"message": inventory})
    except Exception as e:
        response["body"] = json.dumps({"message": f"ERROR: {str(e)}"})

    return response
