import json
import logging
import sys

import boto3

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    name = event['counter']
    logger.info(f'Called with counter={name}')
    try:
        value = fetch_and_update_value(name)
    except Exception as e:
        return exception_handler(e)

    return {
        'statusCode': 200,
        'value': value
    }


def fetch_and_update_value(counter_name):
    table = boto3.resource('dynamodb').Table('hit-counters')
    response = table.get_item(
        Key={'counter-name': counter_name}
    )
    item = response['Item']
    logger.info(f'Item: {item}')
    count = response['Item']['counter-value']
    logger.info(f'Current counter value: {count}')
    count += 1
    response = table.update_item(
        Key={'counter-name': counter_name},
        UpdateExpression="set #countervalue = :v",
        ExpressionAttributeNames={'#countervalue': 'counter-value'},
        ExpressionAttributeValues={':v': count},
        ReturnValues="UPDATED_NEW"
    )
    logger.info(f'Updated counter value: {count}. Update response: {response}')
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
