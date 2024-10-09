#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 11:31:02 2021

@author: mike
"""
import orjson

##############################################
### S3 object key structure
## The keys of the dictionary are the S3 key structure versions.
## 'dataset' contains the dataset metadata for a single dataset.
## 'datasets' contains the dataset metadata for all of the datasets in a single S3 bucket.
## 'station' contains the station data for a single result of a single dataset.
## 'stations' contains the station data for all of the stations in a single dataset.
## 'results' contains the results data chunk for a single station of a single dataset. In the past, the 'results' contained the entire results data of a single station.
## 'results_versions' contains the data about all of the results versions and chunks for all stations in a single dataset.

key_patterns = {
    2: {
        "results": "tethys/v2/{dataset_id}/{station_id}/{run_date}/results.nc.zst",
        "datasets": "tethys/v2/datasets.json.zst",
        "stations": "tethys/v2/{dataset_id}/stations.json.zst",
        "station": "tethys/v2/{dataset_id}/{station_id}/station.json.zst",
        "dataset": "tethys/v2/{dataset_id}/dataset.json.zst",
        "results_object_keys": "tethys/v2/{dataset_id}/results_object_keys.json.zst",
        "diagnostics": "tethys/v2/diagnostics/{run_id}.json.zst",
        "interim_results": "tethys/v2/interim/{run_id}/{dataset_id}/{version_date}/{station_id}.{start_date}.nc.zst",
    },
    3: {
        "results": "tethys/v3/{dataset_id}/{station_id}/{run_date}.results.nc.zst",
        "datasets": "tethys/v3.datasets.json.zst",
        "stations": "tethys/v3/{dataset_id}.stations.json.zst",
        "station": "tethys/v3/{dataset_id}/{station_id}.station.json.zst",
        "dataset": "tethys/v3/{dataset_id}.dataset.json.zst",
        "results_object_keys": "tethys/v3/{dataset_id}.results_object_keys.json.zst",
        "diagnostics": "tethys/v3/diagnostics/{run_id}.json.zst",
        "interim_results": "tethys/v3/interim/{run_id}/{dataset_id}/{version_date}/{station_id}.{start_date}.nc.zst",
    },
    4: {
        "results": "tethys/v4/{dataset_id}/{version_date}/{station_id}/{chunk_id}.results.h5",
        "datasets": "tethys/v4.datasets.json.zst",
        "stations": "tethys/v4/{dataset_id}/{version_date}.stations.json.zst",
        # 'latest_stations': 'tethys/v4/{dataset_id}.stations.json.zst',
        # 'station': 'tethys/v4/{dataset_id}/{version_date}/{station_id}.station.json.zst',
        # 'latest_station': 'tethys/v4/{dataset_id}/{station_id}.station.json.zst',
        "dataset": "tethys/v4/{dataset_id}.dataset.json.zst",
        "versions": "tethys/v4/{dataset_id}.versions.json.zst",
        "results_chunks": "tethys/v4/{dataset_id}/{version_date}.results_chunks.json.zst",
        # 'latest_results_chunks': 'tethys/v4/{dataset_id}.results_chunks.json.zst',
        "diagnostics": "tethys/v4/diagnostics/{run_id}.json.zst",
        "interim_results": "tethys/v4/interim/{run_id}/{dataset_id}/{station_id}.{start_date}.h5",
    },
    5: {
        "results": "tethys/v5/{dataset_id}/{version_date}/{station_id}/{chunk_id}.results.h5",
        "datasets": "tethys/v5.datasets.json.zst",
        "stations": "tethys/v5/{dataset_id}/{version_date}.stations.json.zst",
        "dataset": "tethys/v5/{dataset_id}.dataset.json.zst",
        "versions": "tethys/v5/{dataset_id}.versions.json.zst",
        "results_chunks": "tethys/v5/{dataset_id}/{version_date}.results_chunks.json.zst",
        "diagnostics": "tethys/v5/diagnostics/{run_id}.json.zst",
    },
}

########################################
### Helper functions


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    # return orjson.dumps(v, default=default, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_OMIT_MICROSECONDS | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2).decode()
    return orjson.dumps(
        v,
        default=default,
        option=orjson.OPT_NON_STR_KEYS
        | orjson.OPT_OMIT_MICROSECONDS
        | orjson.OPT_SERIALIZE_NUMPY,
    ).decode()
