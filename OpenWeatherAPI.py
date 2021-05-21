from typing import List
from SecretsManager import SecretsManager
from Datapoint import Datapoint


class OpenWeatherAPI:
    def __init__(self, networkInterface) -> None:
        self.networkInterface = networkInterface
        self.apiKey: str = SecretsManager('openweathermap')['appid']

    def __callAPI(self, zipCode):
        return self.networkInterface.get(f"https://api.openweathermap.org/data/2.5/forecast?zip={zipCode},us&appid={self.apiKey}&cnt=18")

    @staticmethod
    # convert hPa to inHg
    def hPa_inHg(input: float) -> float:
        return 0.02953 * float(input)

    def get(self, zipCode) -> List[Datapoint]:
        response = self.__callAPI(zipCode)['list']
        return [Datapoint(zipCode, item['dt'], self.hPa_inHg(item['main']['pressure'])) for item in response]
