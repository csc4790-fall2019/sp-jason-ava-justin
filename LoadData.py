from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Polarity-Scores')

company = 'Tesla'
ticker = 'TSLA'
polarity = '0.5'
date = '2019-11-29'

'''
response = table.put_item(
   Item={
        'company': company,
        'ticker': ticker,
        'polarity_score': polarity,
        'last_capture_date': date,
    }
)
'''

response = table.get_item(
    Key={
        'company': 'Tesla',
    }
)

response = table.query(
    ProjectionExpression="#yr, title, info.genres, info.actors[0]",
    ExpressionAttributeNames={ "#yr": "year" }, # Expression Attribute Names for Projection Expression only.
    KeyConditionExpression=Key('year').eq(1992) & Key('title').between('A', 'L')
)

for i in response[u'Items']:
    print(json.dumps(i, cls=DecimalEncoder))

print(response)
