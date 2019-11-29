#I ran this script to create the database 

import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='Polarity-Scores',
    KeySchema=[
        {
            'AttributeName': 'Company',
            'KeyType': 'HASH'  #Partition key
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'company',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)
