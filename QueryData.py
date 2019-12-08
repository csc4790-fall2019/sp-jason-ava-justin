from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Polarity-Scores')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# Prints the Database
# response = table.scan()
#
# for i in response['Items']:
#     print(json.dumps(i, cls=DecimalEncoder))

# print("Polarity Scores from April and Company is Google")
# response = table.query(
#     ProjectionExpression="#date, company, polarity_score",
#     ExpressionAttributeNames={ "#date": "date" }, # Expression Attribute Names for Projection Expression only.
#     KeyConditionExpression=Key('company').eq('Facebook') & Key('date').between('2019-04-01', '2019-04-30')
# )
#
# for i in response[u'Items']:
#     print(json.dumps(i, cls=DecimalEncoder))
