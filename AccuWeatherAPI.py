from typing import List
from SecretsManager import SecretsManager
from Datapoint import Datapoint


class AccuWeatherAPI:
    def __init__(self, networkInterface) -> None:
        self.networkInterface = networkInterface
        self.apiKey: str = SecretsManager('accuweather')['apikey']

    def __callAPI(self, locationKey: str):
        return self.networkInterface.get(f'https://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{locationKey}?details=true&apikey={self.apiKey}')

    def get(self, locationKey: str) -> List[Datapoint]:
        response = self.__callAPI(locationKey)
        # NOTE: API currently does not return back pressure!
        return [Datapoint(locationKey, item['EpochDateTime'], item['?']) for item in response]
