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
    """
    Load relevant information about a dataset, giving either custom parameters or the name of a known dataset.

    **Summary:**

        - initialisation:
          `__init__ <#flight_processing.data.GraphBuilder.\_\_init\_\_>`_,
          `known_dataset <#flight_processing.data.GraphBuilder.known_dataset>`_
        - utility:
          `data_flights <#flight_processing.data.GraphBuilder.data_flights>`_,
          `data_graph_yaml <#flight_processing.data.GraphBuilder.data_graph_yaml>`_,
          `data_graph_json <#flight_processing.data.GraphBuilder.data_graph_json>`_,
          `data_graph_npz <#flight_processing.data.GraphBuilder.data_graph_npz>`_,
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

def lerp(x, xmin, xmax, ymin, ymax):
    """
    Linearly interpolate between `ymin` and `ymax` according to the bounds of `xmin` and `xmax`.

    :param x: point to interpolate
    :type x: float
    :param xmin: minimum x value
    :type xmin: float
    :param xmax: maximum x value
    :type xmax: float
    :param ymin: minimum y value
    :type ymin: float
    :param ymax: maximum y value
    :type ymax: float

    :return: resulting y value
    :rtype: float
    """
    if x <= xmin:
        return ymin
    elif x >= xmax:
        return ymax
    else:
        return (((x - xmin) / (xmax - xmin)) * (ymax - ymin)) + ymin
