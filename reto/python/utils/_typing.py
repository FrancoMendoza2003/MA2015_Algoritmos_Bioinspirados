from typing import TypedDict


class DMatrixPayload(TypedDict):
    origins: str
    destinations: str
    travelMode: str
    timeUnit: str
    distanceUnit: str
    startTime: str
