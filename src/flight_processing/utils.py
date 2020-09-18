from datetime import datetime, timedelta

import os
import errno
from pathlib import Path
from appdirs import user_config_dir
import configparser

config_dir = Path(user_config_dir("flight_processing"))
config_file = config_dir / "flight_processing.conf"

if not config_dir.exists():
    config_template = (Path(__file__).parent / "flight_processing.conf").read_text()
    config_dir.mkdir(parents=True)
    config_file.write_text(config_template)

config = configparser.ConfigParser()
config.read(config_file.as_posix())

# defaults
detail = 4
data_prefix = config.get("global", "data_location", fallback="")

format_dataset_location = "{data_prefix}/regions_{dataset}_wkt.json"
format_data_flights = "{data_prefix}/flights/{dataset}/{date}/{time}.json"
format_data_graph = "{data_prefix}/graphs/{dataset}/{date}/{time}.{suffix}"

timestring_traffic = "%Y-%m-%d %H:%M"
timestring_date = "%Y%m%d"
timestring_time = "%H%M"

datasets = dict(
    uk = dict(
        minlon = -11,
        maxlon = 6,
        minlat = 48,
        maxlat = 61.5,
        detail = 7
    ),
    usa = dict(
        minlon = -130,
        maxlon = -58,
        minlat = 23,
        maxlat = 46,
        detail = 4
    ),
    switzerland = dict(
        minlon = 5.3,
        maxlon = 10.7,
        minlat = 45.5,
        maxlat = 48,
        detail = 8
    )
)

class DataConfig:
    def __init__(self, dataset, minlon, maxlon, minlat, maxlat, detail=detail, data_prefix=data_prefix):
        self.dataset = dataset
        self.data_prefix = data_prefix

        self.minlon = minlon
        self.maxlon = maxlon
        self.minlat = minlat
        self.maxlat = maxlat
        self.detail = detail

        self.dataset_location = format_dataset_location.format(data_prefix=data_prefix, dataset=dataset)

        self.bounds_opensky = (self.minlon, self.minlat, self.maxlon, self.maxlat)
        self.bounds_plt = (self.minlon, self.maxlon, self.minlat, self.maxlat)

    @classmethod
    def known_dataset(cls, dataset, data_prefix=data_prefix):
        data = datasets.get(dataset)

        if data is None:
            raise NotImplementedError("Dataset {} not recognised: specify bounds using main __init__ method.".format(dataset))
        else:
            return cls(dataset, data['minlon'], data['maxlon'], data['minlat'], data['maxlat'], data['detail'], data_prefix)


    def data_flights(self, datetime):
        date = datetime.strftime(timestring_date)
        time = datetime.strftime(timestring_time)
        return format_data_flights.format(
                dataset = self.dataset,
                data_prefix = self.data_prefix,
                date = date,
                time = time
        )

    def __data_graph(self, datetime, suffix):
        date = datetime.strftime(timestring_date)
        time = datetime.strftime(timestring_time)
        return format_data_graph.format(
                dataset = self.dataset,
                data_prefix = self.data_prefix,
                date = date,
                time = time,
                suffix = suffix
        )

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

def lerp(x, xmin, xmax, ymin, ymax):
    if x <= xmin:
        return ymin
    elif x >= xmax:
        return ymax
    else:
        return (((x - xmin) / (xmax - xmin)) * (ymax - ymin)) + ymin