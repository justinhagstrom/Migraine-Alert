from typing import Dict


class Datapoint:
    def __init__(self, zipCode, timestamp, pressure) -> None:
        self.zipCode: str = str(zipCode)
        self.timestamp: int = int(timestamp)
        self.pressure: float = round(float(pressure), 5)

    def toDict(self) -> Dict[str, str]:
        return {'zipCode': str(self.zipCode), 'timestamp': str(self.timestamp), 'pressure': str(self.pressure)}
