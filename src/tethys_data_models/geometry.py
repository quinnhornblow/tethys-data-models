#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 16:40:08 2021

@author: mike
"""
from typing import Literal, Union

from pydantic import BaseModel, conlist

# from hashlib import blake2b

################################################3
### Classes

lat_lon = Union[
    conlist(float, min_items=2, max_items=3), conlist(int, min_items=2, max_items=3)
]


class Point(BaseModel):
    """
    Geojson geometry model for points.
    """

    type: Literal["Point"]
    coordinates: lat_lon


class LineString(BaseModel):
    """
    Geojson geometry model for lines.
    """

    type: Literal["LineString"]
    coordinates: conlist(lat_lon, min_items=1)


class MultiPoint(BaseModel):
    """
    Geojson geometry model for multipoints.
    """

    type: Literal["MultiPoint"]
    coordinates: conlist(lat_lon, min_items=1)


class MultiLineString(BaseModel):
    """
    Geojson geometry model for MultiLineString.
    """

    type: Literal["MultiLineString"]
    coordinates: conlist(conlist(lat_lon, min_items=1), min_items=1)


class Polygon(BaseModel):
    """
    Geojson geometry model for Polygon.
    """

    type: Literal["Polygon"]
    coordinates: conlist(conlist(lat_lon, min_items=1), min_items=1)


class MultiPolygon(BaseModel):
    """
    Geojson geometry model for MultiPolygon.
    """

    type: Literal["MultiPolygon"]
    coordinates: conlist(
        conlist(conlist(lat_lon, min_items=1), min_items=1), min_items=1
    )


geometry = Union[Point, LineString, Polygon, MultiLineString, MultiPoint, MultiPolygon]
