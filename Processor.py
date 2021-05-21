from Datapoint import Datapoint
import time


class Processor:
    def __init__(self, databaseInterface) -> None:
        self.db = databaseInterface

    def processDatapoint(self, datapoint: Datapoint) -> bool:
        if self.db.getPressureRecord(datapoint.zipCode, datapoint.timestamp) != datapoint.pressure:
            self.db.addToDB(datapoint)
            return True
        return False

    def processChanges(self, zipCode) -> str:
        now: int = int(time.time())

        # Get records in descending order
        records = self.db.getLatest(zipCode)

        # We are comparing records to look for changes, so we need at least 2
        if len(records) < 2:
            print('Too few records found in DB')
            return ''

        # Filter to include all records in the future plus one record in the past
        i: int = 0
        for record in records:
            if record.timestamp < now:
                break
            i += 1
        records = records[:i+1]

        if len(records) < 2:
            print('Too few records found in DB after postprocessing')
            return ''

        # Put records into ascending order
        records.reverse()

        # Look for change
        current = records[0]
        for i in range(1, len(records)):
            # convert delta seconds to delta hours
            delta_hours = (records[i].timestamp - current.timestamp) / 3600

            # ignore data less than 12 hours long since it is too short term
            if delta_hours < 12:
                continue

            # stop looking past 48 hours
            if delta_hours >= 48:
                break

            delta_pressure = records[i].pressure - current.pressure
            rate = delta_pressure / delta_hours
            print(f'Calculated rate of {rate}')

            # Check for negative rate of change more extreme than 0.3 in/hg per 10 hours
            # timestamp of 0 is hardcoded to represent last notification pressue
            if rate <= -0.03 and round(self.db.getPressureRecord(zipCode, 0), 2) != round(records[i].pressure, 2):
                self.db.addToDB(Datapoint(zipCode, 0, records[i].pressure))
                return f'Migraine Alert: Pressure changing from {round(current.pressure, 2)} to {round(records[i].pressure, 2)} over next {int(delta_hours)} hours.'

        return ''
