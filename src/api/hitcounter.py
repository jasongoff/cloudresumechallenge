import logging
import boto3
import sys
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    name = event['counter']
    logger.info(f'Called with counter={name}')
    try:
        value = get_counter_value(name)
    except Exception as e:
        return exception_handler(e)

    return {
        'statusCode': 200,
        'value': value
    }


def get_counter_value(counter_name):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName='hit-counters',
        Key={'counter-name': {'S': counter_name}}
    )
    item = response['Item']
    logger.info(f'Item: {item}')
    count = response['Item']['counter-value']['N']
    logger.info(f'Counter value: {count}')
    return count


def exception_handler(e):
    error = str(e)
    logger.exception(e)
    status_code = 400
    return {
        'statusCode': status_code,
        'body': json.dumps(error)
    }


if __name__ == "__main__":
    result = lambda_handler({'counter': 'cloud-resume'}, '')
    logger.info(f'{result}')
