import requests
import time


class NetworkInterface:
    def __init__(self) -> None:
        self.madeFirstCall: bool = False

    def __sleep(self) -> None:
        if self.madeFirstCall:
            time.sleep(1)
        else:
            self.madeFirstCall = True

    def get(self, url: str):
        self.__sleep()
        return requests.get(url).json()
