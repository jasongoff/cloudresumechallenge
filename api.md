# Chunk 2: Building the API
To start with, I created and tested the API in a Development account, separate from the Production account hosting the website created in Chunk 1.

## Step 8 - The Database
I started off creating the database via the console to understand exactly what I wanted.

I created a table called `hit-counters` with a partition key of `counter-name (string)`.  

I chose to customise settings and change read/write capacity to On-Demand, to better control costs.

Then, in Explore Items, I added an Item to the Table, and also added a new attribute `counter-value`.  I then had a table:

|counter-name|counter-value|
|---|---|
|cloud-resume|0|

Page 83.

## Step 10 - The Lambda Function and Python Code for the API
Using the console, I created a new function, `getHitCount`, with a basic Lambda role, `getHitCount-role-ljleqr4m`, automatically generated.  

I started simply, ensuring I could pass in the name of a counter and get some return value back.
```python
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    counter_name = event['counter']
    logger.info(f'{counter_name}')
    return {
        'statusCode': 200,
        'value': 12345
    }
```
Next, I extended the function to query DynamoDB to get the current value for my counter.
```python
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    name = event['counter']
    logger.info(f'Called with counter={name}')
    # query DynamoDB table hit-counters to return counter-value where counter-name = name
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName='hit-counters',
        Key={'counter-name': {'S': name}}
    )

    # Process the response
    item = response['Item']
    logger.info(f'Item: {item}')




# Get the current count value
# count = response['Item']['count']['N']

    
    return {
        'statusCode': 200,
        'value': 12345
    }

```
For this to work, I had to create an IAM Policy that allowed read/write access to my DynamoDB table.  I could have assigned the managed Full Access policy, but I wanted to use least privilege.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ReadWriteTable",
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGetItem",
                "dynamodb:GetItem",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:*:*:table/hit-counters"
        },
        {
            "Sid": "GetStreamRecords",
            "Effect": "Allow",
            "Action": "dynamodb:GetRecords",
            "Resource": "arn:aws:dynamodb:*:*:table/hit-counters/stream/* "
        },
        {
            "Sid": "WriteLogStreamsAndGroups",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Sid": "CreateLogGroup",
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "*"
        }
    ]
}
```
I then assigned this policy to the IAM role created when I created the function (`getHitCount-role-ljleqr4m`).  The call to DynamoDB then worked as expected.

Once working, I enhanced the script to increment the counter and write the new value to the DynamoDB table.  The final script is in [src\api\hitcounter.py](src\api\hitcounter.py) and returns a JSON object similar to:
```json
{'statusCode': 200, 'value': Decimal('9')}
```

## Step 9 - Setting up the API using API Gateway
Now that I had a working Lambda function that could return 

## Step 13 - Source Control

