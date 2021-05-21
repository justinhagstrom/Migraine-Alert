from typing import Dict
from Processor import Processor
from DatabaseInterface import DatabaseInterface
from OpenWeatherAPI import OpenWeatherAPI
from NetworkInterface import NetworkInterface
from SNSMessageInterface import SNSMessageInterface
import os


def lambda_handler(event, context) -> None:
    processor: Processor = Processor(DatabaseInterface('barometricPressure'))

    zipCodes: Dict[str, str] = {
        '12345': os.environ['topicArn']}

    for zipCode, topicArn in zipCodes.items():
        if True in [processor.processDatapoint(datapoint) for datapoint in OpenWeatherAPI(NetworkInterface()).get(zipCode)]:
            alert: str = processor.processChanges(zipCode)
            if alert:
                print(f'Sending Alert for zip code {zipCode}: {alert}')
                SNSMessageInterface(topicArn).sendMessage(alert)
