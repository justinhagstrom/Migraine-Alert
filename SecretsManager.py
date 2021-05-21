import boto3  # type: ignore
import json


class SecretsManager:
    def __init__(self, name: str) -> None:
        response = boto3.client(
            'secretsmanager').get_secret_value(SecretId=name)
        self.secret = json.loads(response['SecretString'])

    def __getitem__(self, key: str):
        return self.secret[key]
