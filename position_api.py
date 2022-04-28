# https://docs.altitudeangel.com/docs/surveillance-api

from datetime import datetime
from typing import List, Optional

import httpx
from pydantic import BaseModel

from settings import settings


# Data Models


class GeographicPosition(BaseModel):
    lat: float  # the latitude in decimal degrees
    lon: float  # the longitude in decimal degrees
    # Accuracy of the position in meters. If not specified, accuracy is assumed to be
    # the accuracy of the lat/long provided
    accuracy: Optional[float]
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
    # Text string describing the type of identifier, (e.g. ICAO, IMEI, SerialNumber)
    type: Optional[str]


class Target(BaseModel):
    sourceId: Optional[str]  # The sensor's unique id for this target
    # The type of target detected in a urn format. One of "aa:target:aircraft"
    # or "aa:target:drone"
    type: Optional[str]
    # The percentage confidence that the type has been identified correctly (1-100)
    confidence: Optional[int]
    ids: Optional[List[Identifier]]  # Collection of known identifiers for this target
    # JSON - Additional information about the target, e.g. make, model
    additionalInfo: Optional[str]


class PositionData(BaseModel):
    id: str  # Uniquely identifies this specific position report by the sender
    # Indicates when the position report was sent, according to the sensor clock,
    # in UTC. # (IAT should be accounted for by the sensor)
    sourceTimeStamp: datetime
    position: GeographicPosition  # Contains the position of the detected object
    target: Optional[Target]  # Contains identification details of the detected object
    # Contains one or more detected altitudes for the object
    altitudes: Optional[List[Height]]
    # Contains data for the speed (in m/s) and track of the object.
    groundVelocity: Optional[GeographicVector]
    # Contains information about the true airspeed (TAS) of the object
    trueAirspeed: Optional[GeographicVector]
    # True if the sensor considers the object to be on the ground
    onGround: Optional[bool]
    # Contains acceleration information for the object
    acceleration: Optional[GeographicVector]
    heading: Optional[float]  # Object heading in degrees
    # JSON - Provides any additional sensor-specific information
    additionalInfo: Optional[str]


class SensorPosition(BaseModel):
    # The position of the sensor providing the positions
    geographicPosition: Optional[GeographicPosition]
    # The altitude of the sensor. For ground-based sensors, altitude datum should be MSL
    altitude: Optional[Height]
    # For directed sensors, the direction it is facing in degrees from north
    heading: Optional[float]
    # For directed sensors, the angle of the device in degrees from horizontal
    angle: Optional[float]


class SensorState(BaseModel):
    id: str  # The locally unique identifier of the sensor providing the positions
    pressure: Optional[float]  # Current pressure in mb at the sensor's location
    # Provides up to date sensor position information if the sensor can move/rotate/etc.
    sensorPosition: Optional[SensorPosition]
    # JSON - Provides any additional information about the current state of the sensor
    additionalInfo: Optional[str]


class PositionReport(BaseModel):
    # Metadata about the sensor device providing positions
    sensor: Optional[SensorState]
    positions: List[PositionData]  # Collection of positions. Must not be empty


# API Calls


def send_position_report(access_token, position_report):
    """
    The API receives position reports which are processed asynchronously.

    A position report consists of the following key pieces of data:

    sensor metadata identifying the sensor for which data is submitted
    One (or more) positions, which specify information about objects known, or visible,
    to the sensor

    :param access_token: access token obtained by using auth_api.py
    :param position_report: instance of the class PositionReport
    :return:
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    return httpx.post(
        settings.position_uri,
        headers=headers,
        data=position_report.json(exclude_unset=True),
    )
