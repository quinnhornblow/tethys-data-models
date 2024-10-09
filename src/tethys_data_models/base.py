#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 13:46:09 2021

@author: mike
"""
from typing import Dict

# from hashlib import blake2b
import orjson
from pydantic import BaseModel, Field, HttpUrl

from tethys_data_models.geometry import geometry
from tethys_data_models.utils import orjson_dumps

##############################################3
### Base models


class ConnectionConfig(BaseModel):
    service_name: str
    endpoint_url: HttpUrl
    aws_access_key_id: str
    aws_secret_access_key: str


class Remote(BaseModel):
    bucket: str
    connection_config: ConnectionConfig = None
    public_url: HttpUrl = None
    version: int = Field(..., description="Version of the S3 data structure.")
    description: str = Field(
        None,
        description="Description of the datasets that are contained within the remote.",
    )


class Station(BaseModel):
    """
    Contains the base station data.
    """

    station_id: str = Field(..., description="station id based on the geometry")
    ref: str = Field(None, description="station reference ID given by owner")
    name: str = None
    osm_id: int = None
    geometry: geometry
    altitude: float = None
    properties: Dict = Field(
        None, description="Any additional station specific properties."
    )

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
