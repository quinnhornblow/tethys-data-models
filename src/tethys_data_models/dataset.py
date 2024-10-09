"""
Created by Mike Kittridge on 2020-11-02.

For hashing the geometry of stations, use blake2b with a digest_size of 12 of the hex encoded WKB.
Similar for the dataset_id, except that the first 8 fields (starting with feature) of the dataset dict should be used for the hashing.
"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Literal, Union

import orjson
from pydantic import BaseModel, Field, HttpUrl, confloat, conint

from tethys_data_models import base
from tethys_data_models.geometry import geometry
from tethys_data_models.utils import orjson_dumps

#########################################
### Models


class ResultType(str, Enum):
    time_series = "time_series"
    grid = "grid"
    trajectory = "trajectory"
    time_series_bands = "time_series_bands"
    grid_bands = "grid_bands"
    trajectory_bands = "trajectory_bands"


class TimeSeriesDims(BaseModel):
    time: int
    geometry: int
    height: int


class GridDims(BaseModel):
    time: int
    lat: int
    lon: int
    height: int


class TrajectoryDims(BaseModel):
    time: int


class TimeSeriesBandsDims(BaseModel):
    time: int
    geometry: int
    height: int
    band: int


class GridBandsDims(BaseModel):
    time: int
    lat: int
    lon: int
    height: int
    band: int


class TrajectoryBandsDims(BaseModel):
    time: int
    band: int


ResultDims = Union[
    TimeSeriesDims,
    GridDims,
    TrajectoryDims,
    TimeSeriesBandsDims,
    GridBandsDims,
    TrajectoryBandsDims,
]

result_type_dict = {
    "time_series": TimeSeriesDims,
    "grid": GridDims,
    "trajectory": TrajectoryDims,
    "time_series_bands": TimeSeriesBandsDims,
    "grid_bands": GridBandsDims,
    "trajectory_bands": TrajectoryBandsDims,
}


class TimeRange(BaseModel):
    """ """

    from_date: datetime
    to_date: datetime


# class Stats(BaseModel):
#     """
#     Statistics related to the results.
#     """
#     min: float
#     max: float
#     mean: float
#     median: float
#     count: int


class ChunkParams(BaseModel):
    block_length: confloat(ge=0) = Field(
        ...,
        description="The length in decimal degrees of the sides of the block/square for the spatial grouping. A value of 0 indicates that all geometries or lat/lon combos are split individually.",
    )
    time_interval: conint(gt=0) = Field(
        ...,
        description="The chunk time interval is the number of days the time chunk should cover (e.g. 7 would be a week).",
    )


class ResultChunk(BaseModel):
    """
    Contain the data about a chunk object of a result.
    """

    chunk_id: str = Field(
        ..., description="The chunk id that is unique within this station."
    )
    key: str = Field(
        ...,
        description="The S3 key where this results chunk is stored. This will be totally unique for this results chunk.",
    )
    # bucket: str
    content_length: conint(gt=0)
    # etag: str
    # obj_id: str = Field(..., description='This is the version id given by the S3 API response when using a put_object call.')
    version_date: datetime = Field(
        ...,
        description="The date that uniquely defines this results chunk version of the dataset and station.",
    )
    chunk_hash: str = Field(
        ..., description="The hash of the results data stored in the chunk."
    )
    dataset_id: str = Field(..., description="The dataset uuid.")
    station_id: str = Field(..., description="station id based on the geometry.")
    height: int = Field(
        ...,
        description="The height multiplied by 1000 (so that it is in mm). Should be omitted if the results do not have height as part of the dimensions.",
    )
    chunk_day: conint(ge=-106751, le=106751) = Field(
        ...,
        description="The start day of the interval for this chunk. The chunk day is the number of days after 1970-01-01. Can be negative for days before 1970-01-01 with a minimum of -106751, which is 1677-09-22 (minimum possible date). The maximum value is 106751.",
    )
    band: conint(ge=0) = Field(
        None,
        description="The band (starting with 0) of the bands array of the results. Should be omitted if the results do not have band as part of the dimensions.",
    )
    n_times: conint(ge=0) = Field(
        None, description="The length of the time dimension array."
    )
    from_date: datetime
    to_date: datetime
    modified_date: datetime = Field(
        ..., description="The modification date of the last edit."
    )

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ResultVersion(BaseModel):
    """
    Contains information about results versions for a dataset.
    """

    dataset_id: str = Field(..., description="The dataset uuid.")
    version_date: datetime = Field(
        ...,
        description="The date that uniquely defines this results version of the dataset and station.",
    )
    name: str = None
    doi: HttpUrl = Field(
        None,
        description="The digital object identifier (DOI) for this specific version of the dataset. This should be in the form of an http URL.",
    )
    description: str = Field(None, description="Description of the results version.")
    modified_date: datetime = Field(
        ..., description="The modification date of the last edit."
    )

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


# class ResultVersionGroup(BaseModel):
#     """
#     Groups many result versions together with the dataset_id and station_id. This is to be saved to the *.results_versions.json.zst object with all of the other stations.
#     """
#     dataset_id: str = Field(..., description='The dataset uuid.')
#     station_id: str = Field(..., description='station id based on the geometry')
#     result_versions: List[ResultVersion]
#
#     class Config:
#         json_loads = orjson.loads
#         json_dumps = orjson_dumps


# class ResultVersionGroup(BaseModel):
#     """
#     Groups many result versions and chunks together with the dataset_id. This is to be saved to the *.results_versions.json.zst object with all of the other stations.
#     """
#     # dataset_id: str = Field(..., description='The dataset uuid.')
#     results_versions: List[ResultVersion]
#     results_chunks: List[ResultChunk]

#     class Config:
#         json_loads = orjson.loads
#         json_dumps = orjson_dumps


class Station(base.Station):
    """
    Contains the station data.
    """

    dataset_id: str = Field(..., description="The dataset uuid.")
    dimensions: ResultDims
    time_range: TimeRange = Field(
        ..., description="The maximum time range of the result."
    )
    heights: Union[List[float], List[int]]
    bands: List[int] = None
    modified_date: datetime = Field(
        ..., description="The modification date of the last edit."
    )


# class Station(StationBase):
#     """
#     Contains the complete station data.
#     """
#     results_chunks: List[ResultChunk]
#     content_length: conint(gt=0)
#     modified_date: datetime = Field(..., description='The modification date of the last edit.')


# class StationAgg(StationBase):
#     """
#     Contains the complete station data, but does not include the results chunks. version. This object is meant to be combined with all of the other stations in a dataset (i.e. the *.stations.json.zst file).
#     """
#     modified_date: datetime = Field(..., description='The modification date of the last edit.')


class DatasetBase(BaseModel):
    """
    Core fields in the dataset metadata to create the dataset_id.
    """

    feature: str = Field(
        ..., description="The geographic feature associated with the dataset."
    )
    parameter: str = Field(..., description="The observation parameter name.")
    method: str = Field(
        ..., description="The way the recorded observation was obtained."
    )
    product_code: str = Field(
        ...,
        description="The code associated with kind of product produced. This could be generic codes like raw_data or quality_controlled; or it could be more uniquely identifying the simulation product that was produced.",
    )
    owner: str = Field(
        ..., description="The operator, owner, and/or producer of the associated data."
    )
    aggregation_statistic: str = Field(
        ...,
        description="The statistic that defines how the result was calculated. The aggregation statistic is calculated over the time frequency interval associated with the recorded observation.",
    )
    frequency_interval: str = Field(
        ...,
        description="The frequency that the observation was recorded at. In the form 1H for hourly or 24H for daily. A value of T indicates that the data is saved at its instantaneous measured value (usually down to the minute precision).",
    )
    utc_offset: str = Field(
        ...,
        description="The offset time from UTC associated with the frequency_interval. For example, if data was collected daily at 9:00 in the timezone of UTC+12, then the frequency_interval would be 24H and the utc_offset would be -3H. This parameter is most important for frequency intervals equal to or greater than 24H and must allign the day with UTC. The offset must be smaller than the frequency_interval.",
    )


class Dataset(DatasetBase):
    """
    Full dataset metadata schema.
    """

    dataset_id: str = Field(
        ...,
        description="The unique dataset id based on the felds in the DatasetBase model.",
    )
    units: str = Field(..., description="The units of the results.")
    license: str = Field(
        ...,
        description="The legal data license associated with the dataset defined by the owner.",
    )
    attribution: str = Field(
        ...,
        description="The legally required attribution text to be distributed with the data defined by the owner.",
    )
    result_type: ResultType = Field(
        ..., description="This describes how the results are structurally stored."
    )
    extent: geometry = Field(
        None,
        description="The geographical extent of the datset as a simple rectangular polygon.",
    )
    time_range: TimeRange = Field(
        None, description="The maximum time range of the dataset."
    )
    spatial_resolution: float = Field(
        None,
        description="The spatial resolution in decimal degrees if the result_type is grid.",
    )
    cf_standard_name: str = Field(
        None, description="The CF conventions standard name for the parameter."
    )
    wrf_standard_name: str = Field(
        None, description="The WRF standard name for the parameter."
    )
    precision: float = Field(
        ..., description="The decimal precision of the result values."
    )
    description: str = Field(None, description="Dataset description.")
    product_description: str = Field(
        None, description="Overall description of the product if method."
    )
    parent_datasets: List[str] = Field(
        None, description="The parent datasets that this dataset was derived from."
    )
    properties: Dict = Field(
        None, description="Any additional dataset specific properties."
    )
    modified_date: datetime = Field(
        None, description="The modification date of the last edit."
    )
    system_version: conint(gt=1) = Field(
        None, description="The version of the metadata structure."
    )
    heights: Union[List[float], List[int]] = Field(
        None, description="The heights from all available results in the dataset."
    )
    bands: List[conint(ge=0)] = None
    chunk_parameters: ChunkParams
    crs: str = Field(
        None, description="The geographic coordinate system as a proj4 string."
    )

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ParameterAttrs(DatasetBase):
    """ """

    dataset_id: str = Field(
        ...,
        description="The unique dataset id based on the felds in the DatasetBase model.",
    )
    units: str = Field(..., description="The units of the results.")
    license: str = Field(
        ...,
        description="The legal data license associated with the dataset defined by the owner.",
    )
    attribution: str = Field(
        ...,
        description="The legally required attribution text to be distributed with the data defined by the owner.",
    )
    result_type: ResultType = Field(
        ..., description="This describes how the results are structurally stored."
    )
    cf_standard_name: str = Field(
        None, description="The CF conventions standard name for the parameter."
    )
    wrf_standard_name: str = Field(
        None, description="The WRF standard name for the parameter."
    )
    precision: float = Field(
        None, description="The decimal precision of the result values."
    )
    description: str = Field(None, description="Dataset description.")
    block_length: confloat(ge=0) = Field(
        ...,
        description="The length in decimal degrees of the sides of the block/square for the spatial grouping. A value of 0 indicates that all geometries or lat/lon combos are split individually.",
    )
    time_interval: conint(gt=0) = Field(
        ...,
        description="The chunk time interval is the number of days the time chunk should cover (e.g. 7 would be a week).",
    )


# class ResultAttrs(BaseModel):
#     """
#     The result attributes that should be in the results netcdf file.
#     """
#     result_type: ResultType
#     title: str
#     institution: str
#     license: str
#     source: str
#     history: str
#     version: int


class ChunkID(BaseModel):
    """
    Model to define the hashing dict to create the chunk_id.
    """

    # station_id: str = Field(..., description='station id based on the geometry')
    height: int = Field(
        None,
        description="The height multiplied by 1000 (so that it is in mm). Should be omitted if the results do not have height as part of the dimensions.",
    )
    chunk_day: conint(ge=-106751, le=106751) = Field(
        ...,
        description="The start day of the interval for this chunk. The chunk day is the number of days after 1970-01-01. Can be negative for days before 1970-01-01 with a minimum of -106751, which is 1677-09-22 (minimum possible date). The maximum value is 106751.",
    )
    band: conint(ge=0) = Field(
        None,
        description="The band (starting with 0) of the bands array of the results. Should be omitted if the results do not have band as part of the dimensions.",
    )

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ResultsEncoding(BaseModel):
    """
    The encoding model for saving xarray Datasets to netcdf.
    """

    scale_factor: float
    dtype: Literal["int8", "int16", "int32", "int64"]
    _FillValue: int


# class Result(BaseModel):
#     """
#     A normal time series result.
#     """
#     dataset_id: str = Field(..., description='The unique dataset uuid.')
#     station_id: str = Field(..., description='station uuid')
#     from_date: Union[datetime, date] = Field(..., description='The start datetime of the observation.')
#     result: Union[str, int, float] = Field(..., description='The recorded observation parameter.')
#     quality_code: str = Field(None, description='The censor_code of the observation. E.g. > or <')
#     censor_code: str = Field(None, description='The censor_code of the observation. E.g. > or <')
#     properties: Dict = Field(None, description='Any additional result specific properties.')
#     modified_date: datetime = Field(None, description='The modification date of the last edit.')


############################################
### Testing

# import fastjsonschema
#
# station_schema = station.schema()
#
# geometry = {'type': 'Point', 'coordinates': [10000.2334, 344532.3451]}
#
# station_dict = dict(station_id='123', virtual_station=False, geometry=geometry)
#
# station1 = station(**station_dict)
#
# station(station_id='123', virtual_station=False, geometry=geometry).dict(exclude_none=True)
#
#
# val1 = fastjsonschema.compile(station_schema)
#
# val1(station_dict)
