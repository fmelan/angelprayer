# https://docs.altitudeangel.com/docs/surveillance-api

from datetime import datetime
from typing import List, Optional

import httpx
from pydantic import BaseModel

test_position_uri = "https://surveillance-api.sit.altitudeangel.io/v1/position-reports"


# Data Models


class GeographicPosition(BaseModel):
    lat: float  # the latitude in decimal degrees
    lon: float  # the longitude in decimal degrees
    accuracy: Optional[float]  # Accuracy of the position in meters. If not specified, accuracy is assumed to be the accuracy of the lat/long provided
    source: Optional[str]  # Indicates the source of the position data (e.g GPS)
    age: Optional[float]  # The age in seconds since this data was acquired


class GeographicVector(BaseModel):
    x: Optional[float]  # East-West part of the vector
    y: Optional[float]  # North-South part of the vector
    z: Optional[float]  # Up-Down part of the vector
    horizontalAccuracy: Optional[float]  # Accuracy of the x/y parts
    verticalAccuracy: Optional[float]  # Accuracy of the z part
    source: Optional[float]  # The source of the vector information
    age: Optional[float]  # The age in seconds since this data was acquired


class Height(BaseModel):
    height: float  # The height in meters according to the specified datum
    datum: str  # The height datum. One of “wgs84”, “agl”, “bar”, “msl”
    accuracy: Optional[float]  # Accuracy of the height in meters
    source: Optional[str]  # The source of the height data
    age: Optional[float]  # The age in seconds since this data was acquired


class Identifier(BaseModel):
    id: str  # The id value
    type: Optional[str]  # Text string describing the type of identifier, (e.g. ICAO, IMEI, SerialNumber)


class Target(BaseModel):
    sourceId: Optional[str]  # The sensor's unique id for this target
    type: Optional[str]  # The type of target detected in a urn format. One of "aa:target:aircraft" or "aa:target:drone"
    confidence: Optional[int]  # The percentage confidence that the type has been identified correctly (1-100)
    ids: Optional[List[Identifier]]  # Collection of known identifiers for this target
    additionalInfo: Optional[str]  # JSON - Additional information about the target, e.g. make, model


class PositionData(BaseModel):
    id: str  # Uniquely identifies this specific position report by the sender
    sourceTimeStamp: datetime  # Indicates when the position report was sent, according to the sensor clock, in UTC. # (IAT should be accounted for by the sensor)
    position: GeographicPosition  # Contains the position of the detected object
    target: Optional[Target]  # Contains identification details of the detected object
    altitudes: Optional[List[Height]]  # Contains one or more detected altitudes for the object
    groundVelocity: Optional[GeographicVector]  # Contains data for the speed (in m/s) and track of the object.
    trueAirspeed: Optional[GeographicVector]  # Contains information about the true airspeed (TAS) of the object
    onGround: Optional[bool]  # True if the sensor considers the object to be on the ground
    acceleration: Optional[GeographicVector]  # Contains acceleration information for the object
    heading: Optional[float]  # Object heading in degrees
    additionalInfo: Optional[str]  # JSON - Provides any additional sensor-specific information


class SensorPosition(BaseModel):
    geographicPosition: Optional[GeographicPosition]  # The position of the sensor providing the positions
    altitude: Optional[Height]  # The altitude of the sensor. For ground-based sensors, altitude datum should be MSL
    heading: Optional[float]  # For directed sensors, the direction it is facing in degrees from north
    angle: Optional[float]  # For directed sensors, the angle of the device in degrees from horizontal


class SensorState(BaseModel):
    id: str  # The locally unique identifier of the sensor providing the positions
    pressure: Optional[float]  # Current pressure in mb at the sensor's location
    sensorPosition: Optional[SensorPosition]  # Provides up to date sensor position information if the sensor can move/rotate/etc.
    additionalInfo: Optional[str]  # JSON - Provides any additional information about the current state of the sensor


class PositionReport(BaseModel):
    sensor: Optional[SensorState]  # Metadata about the sensor device providing positions
    positions: List[PositionData]  # Collection of positions. Must not be empty


# API Calls


def send_position_report(access_token, position_report):
    """
    The API receives position reports which are processed asynchronously.

    A position report consists of the following key pieces of data:

    sensor metadata identifying the sensor for which data is submitted
    One (or more) positions, which specify information about objects known, or visible, to the sensor

    :param access_token: access token obtained by using auth_api.py
    :param position_report: instance of the class PositionReport
    :return:
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    return httpx.post(test_position_uri, headers=headers, data=position_report.json(exclude_unset=True))
