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
    conlist(float, min_length=2, max_length=3), conlist(int, min_length=2, max_length=3)
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
    coordinates: list[lat_lon]


class MultiPoint(BaseModel):
    """
    Geojson geometry model for multipoints.
    """

    type: Literal["MultiPoint"]
    coordinates: list[lat_lon]


class MultiLineString(BaseModel):
    """
    Geojson geometry model for MultiLineString.
    """

    type: Literal["MultiLineString"]
    coordinates: list[list[lat_lon]]


class Polygon(BaseModel):
    """
    Geojson geometry model for Polygon.
    """

    type: Literal["Polygon"]
    coordinates: list[list[lat_lon]]


class MultiPolygon(BaseModel):
    """
    Geojson geometry model for MultiPolygon.
    """

    type: Literal["MultiPolygon"]
    coordinates: list[list[list[lat_lon]]]


geometry = Union[Point, LineString, Polygon, MultiLineString, MultiPoint, MultiPolygon]
