from datetime import datetime, timedelta

import os
import errno
from pathlib import Path
from appdirs import user_config_dir
import configparser
import numpy as np

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
    """
    Load relevant information about a dataset, giving either custom parameters or the name of a known dataset.

    **Summary:**

        - initialisation:
          `__init__ <#flight_processing.DataConfig.\_\_init\_\_>`_,
          `known_dataset <#flight_processing.DataConfig.known_dataset>`_
        - properties:
          `dataset <#flight_processing.DataConfig.dataset>`_,
          `minlon <#flight_processing.DataConfig.minlon>`_,
          `maxlon <#flight_processing.DataConfig.maxlon>`_,
          `minlat <#flight_processing.DataConfig.minlat>`_,
          `maxlat <#flight_processing.DataConfig.maxlat>`_,
          `detail <#flight_processing.DataConfig.detail>`_,
          `dataset_location <#flight_processing.DataConfig.dataset_location>`_,
          `bounds_opensky <#flight_processing.DataConfig.bounds_opensky>`_,
          `bounds_plt <#flight_processing.DataConfig.bounds_plt>`_
        - utility:
          `data_flights <#flight_processing.DataConfig.data_flights>`_,
          `data_graph_yaml <#flight_processing.DataConfig.data_graph_yaml>`_,
          `data_graph_json <#flight_processing.DataConfig.data_graph_json>`_,
          `data_graph_npz <#flight_processing.DataConfig.data_graph_npz>`_
    """

    def __init__(self, dataset, minlon, maxlon, minlat, maxlat, detail=detail, data_prefix=data_prefix):
        """
        Initialise the object with custom parameters.

        :param dataset: dataset name
        :type dataset: str
        :param minlon: longitude minimum bound
        :type minlon: float
        :param maxlon: longitude maximum bound
        :type maxlon: float
        :param minlat: latitude minimum bound
        :type minlat: float
        :param maxlat: latitude maximum bound
        :type maxlat: float
        :param detail: map detail on plots
        :type detail: int, optional
        :param data_prefix: dataset folder location, overrides config
        :type data_prefix: str, optional

        :return: object
        :rtype: DataConfig
        """

        self.__dataset = dataset
        self.data_prefix = data_prefix

        self.__minlon = minlon
        self.__maxlon = maxlon
        self.__minlat = minlat
        self.__maxlat = maxlat
        self.__detail = detail

        self.__dataset_location = format_dataset_location.format(data_prefix=data_prefix, dataset=dataset)

        self.__bounds_opensky = (self.__minlon, self.__minlat, self.__maxlon, self.__maxlat)
        self.__bounds_plt = (self.__minlon, self.__maxlon, self.__minlat, self.__maxlat)

    @classmethod
    def known_dataset(cls, dataset, data_prefix=data_prefix):
        """
        Initialise the object with known parameters.

        :param dataset: dataset name
        :type dataset: str
        :param data_prefix: dataset folder location, overrides config
        :type data_prefix: str, optional

        :return: object
        :rtype: DataConfig
        """
        data = datasets.get(dataset)

        if data is None:
            raise NotImplementedError("Dataset {} not recognised: specify bounds using main __init__ method.".format(dataset))
        else:
            return cls(dataset, data['minlon'], data['maxlon'], data['minlat'], data['maxlat'], data['detail'], data_prefix)

    @property
    def dataset(self):
        """
        Returns the name of the dataset.

        :rtype: str
        """
        return self.__dataset

    @property
    def minlon(self):
        """
        Returns the longitude minimum bound.

        :rtype: float
        """
        return self.__minlon

    @property
    def maxlon(self):
        """
        Returns the longitude maximum bound.

        :rtype: float
        """
        return self.__maxlon

    @property
    def minlat(self):
        """
        Returns the latitude minimum bound.

        :rtype: float
        """
        return self.__minlat

    @property
    def maxlat(self):
        """
        Returns the latitude maximum bound.

        :rtype: float
        """
        return self.__maxlat

    @property
    def detail(self):
        """
        Returns the map detail.

        :rtype: int
        """
        return self.__detail

    @property
    def dataset_location(self):
        """
        Returns the location of the saved geopandas GeoDataFrame.

        :rtype: str
        """
        return self.__dataset_location

    @property
    def bounds_opensky(self):
        """
        Returns the bounding box of the dataset in the format expected by traffic.

        :rtype: (float, float, float, float)
        """
        return self.__bounds_opensky

    @property
    def bounds_plt(self):
        """
        Returns the bounding box of the dataset in the format expected by pyplot.

        :rtype: (float, float, float, float)
        """
        return self.__bounds_plt

    def data_flights(self, datetime):
        """
        Get the location of a flight dump for the given datetime.

        :param datetime: datetime to get
        :type datetime: datetime.datetime or str

        :return: location of file (may not exist)
        :rtype: str
        """
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
        """
        Get the location of a YAML graph for the given datetime.

        :param datetime: datetime to get
        :type datetime: datetime.datetime or str

        :return: location of file (may not exist)
        :rtype: str
        """
        return self.__data_graph(datetime, "yaml")

    def data_graph_json(self, datetime):
        """
        Get the location of a JSON graph for the given datetime.

        :param datetime: datetime to get
        :type datetime: datetime.datetime or str

        :return: location of file (may not exist)
        :rtype: str
        """
        return self.__data_graph(datetime, "json")

    def data_graph_npz(self, datetime):
        """
        Get the location of an NPZ graph for the given datetime.

        :param datetime: datetime to get
        :type datetime: datetime.datetime or str

        :return: location of file (may not exist)
        :rtype: str
        """
        return self.__data_graph(datetime, "npz")


def check_file(filename):
    """
    Given a filename check if its parent directory exists, creating any necessary directories if not.

    :param filename: filename to check
    :type filename: str
    """
    if filename is not None and not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def execute_bulk(function, time_start, count, time_delta=None):
    """
    Execute the given function multiple times, stepping through time as its parameter.

    Running `execute_bulk(f, t0, 2, d)` will execute `f(t0 + 0*d, t0 + 1*d)` followed by `f(t0 + 1*d, t0 + 2*d)`.

    :param function: function to execute, must take 2 datetime arguments
    :type function: function
    :param time_start: start time
    :type time_start: datetime.datetime
    :param count: number of times to run the function
    :type count: int
    :param time_delta: amount by which to increase the time each step, defaults to datetime.timedelta(hours=1)
    :type time_delta: datetime.timedelta
    """
    time_delta = time_delta if time_delta is not None else timedelta(hours=1)
    for i in range(count):
        t1 = time_start + (i * time_delta)
        t2 = time_start + ((i + 1) * time_delta)
        function(t1, t2)

def execute_bulk_between(function, time_start, time_end, time_delta=None):
    """
    Execute the given function multiple times, stepping through time as its parameter.
    Stops when `time_end` is reached.

    :param function: function to execute, must take 2 datetime arguments
    :type function: function
    :param time_start: start time
    :type time_start: datetime.datetime
    :param time_end: end time
    :type time_end: datetime.datetime
    :param time_delta: amount by which to increase the time each step, defaults to datetime.timedelta(hours=1)
    :type time_delta: datetime.timedelta
    """
    time_delta = time_delta if time_delta is not None else timedelta(hours=1)
    t1 = time_start
    t2 = time_start + time_delta
    while t2 <= time_end:
        function(t1, t2)
        t1 += time_delta
        t2 += time_delta

def lerp(x, x1, x2, y1, y2):
    """
    Linearly interpolate between ``y1`` and ``y2`` according to the bounds of ``x1`` and ``x2``.

    It must hold that ``x1 >= x2`` - this function is designed to create a
    gradient which approaches its maximum value as ``x`` moves down from ``x1``
    to ``x2``.

    :param x: point to interpolate
    :type x: float
    :param x1: maximum x value
    :type x1: float
    :param x2: minimum x value
    :type x2: float
    :param y1: minimum y value
    :type y1: float
    :param y2: maximum y value
    :type y2: float

    :return: resulting y value
    :rtype: float
    """

    assert(x1 >= x2)

    return float(np.interp(-x, [-x1, -x2], [y1, y2]))