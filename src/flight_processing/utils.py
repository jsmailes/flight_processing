from datetime import datetime, timedelta
from . import config

import os
import errno

# defaults
dataset = "usa"
data_prefix = config.get("global", "data_location", fallback="")


format_dataset_location = "{data_prefix}/regions_{dataset}_wkt.json"
format_data_flights = "{data_prefix}/flights/{dataset}/{date}/{time}.json"
format_data_graph = "{data_prefix}/graphs/{dataset}/{date}/{time}.{suffix}"

timestring_traffic = "%Y-%m-%d %H:%M"
timestring_date = "%Y%m%d"
timestring_time = "%H%M"

class DataConfig:
    def __init__(self, dataset=dataset, data_prefix=data_prefix):
        self.dataset = dataset
        self.data_prefix = data_prefix

        if dataset == "uk":
            self.minlon = -11
            self.maxlon = 6
            self.minlat = 48
            self.maxlat = 61.5
            self.detail = 6
        elif dataset == "usa":
            self.minlon = -130
            self.maxlon = -58
            self.minlat = 23
            self.maxlat = 46
            self.detail = 4
        elif dataset == "switzerland":
            self.minlon = 5.3
            self.maxlon = 10.7
            self.minlat = 45.5
            self.maxlat = 48
            self.detail = 6
        else:
            raise NotImplementedError("Dataset not recognised!")

        self.dataset_location = format_dataset_location.format(data_prefix=data_prefix, dataset=dataset)

        self.bounds_opensky = (self.minlon, self.minlat, self.maxlon, self.maxlat)
        self.bounds_plt = (self.minlon, self.maxlon, self.minlat, self.maxlat)

    def data_flights(self, datetime):
        date = datetime.strftime(timestring_date)
        time = datetime.strftime(timestring_time)
        return format_data_flights.format(
                dataset = self.dataset,
                data_prefix = self.data_prefix,
                date = date,
                time = time)

    def __data_graph(self, datetime, suffix):
        date = datetime.strftime(timestring_date)
        time = datetime.strftime(timestring_time)
        return format_data_graph.format(
                dataset = self.dataset,
                data_prefix = self.data_prefix,
                date = date,
                time = time,
                suffix = suffix)

    def data_graph_yaml(self, datetime):
        return self.__data_graph(datetime, "yaml")

    def data_graph_json(self, datetime):
        return self.__data_graph(datetime, "json")

    def data_graph_npz(self, datetime):
        return self.__data_graph(datetime, "npz")


def check_file(filename):
    if filename is not None and not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def execute_bulk(function, time_start, count, time_delta=None):
    time_delta = time_delta if time_delta is not None else timedelta(hours=1)
    for i in range(count):
        t1 = time_start + (i * time_delta)
        t2 = time_start + ((i + 1) * time_delta)
        function(t1, t2)

def execute_bulk_between(function, time_start, time_end, time_delta=None):
    time_delta = time_delta if time_delta is not None else timedelta(hours=1)
    t1 = time_start
    t2 = time_start + time_delta
    while t2 <= time_end:
        function(t1, t2)
        t1 += time_delta
        t2 += time_delta