import boto3  # type: ignore
from boto3.dynamodb.conditions import Key  # type: ignore
from Datapoint import Datapoint


class DatabaseInterface:
    def __init__(self, tableName: str):
        self.table = boto3.resource('dynamodb').Table(tableName)

    def getPressureRecord(self, zipCode, timestamp):
        response = self.table.get_item(
            Key={'zipCode': str(zipCode), 'timestamp': str(timestamp)})
        if 'Item' in response:
            return round(float(response['Item']['pressure']), 5)
        return 0

    def addToDB(self, datapoint) -> None:
        self.table.put_item(Item=datapoint.toDict())

    def getLatest(self, zipCode):
        response = self.table.query(
            KeyConditionExpression=Key('zipCode').eq(zipCode),
            Limit=42,
            ConsistentRead=True,
            ScanIndexForward=False  # Decending order, newest timestamp first
        )
        if 'Items' in response and len(response['Items']):
            return [Datapoint(zipCode, item['timestamp'], item['pressure']) for item in response['Items']]
        return []
