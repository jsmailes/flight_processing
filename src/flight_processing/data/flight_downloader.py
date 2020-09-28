from ..utils import DataConfig, check_file, execute_bulk, execute_bulk_between

from datetime import timedelta
from dateutil import parser

from traffic.data import opensky
import simplejson

import sys
import logging

logger = logging.getLogger(__name__)

timestring_traffic = "%Y-%m-%d %H:%M"

def flights_to_json(flights):
    """
    Convert flights to JSON for exporting.

    :param flights: flights to save
    :type flights: traffic.core.traffic.Traffic

    :return: JSON output
    :rtype: str
    """

    flight_coords = []

    logger.info("Converting flights to list of coordinates.")

    if flights is not None:
        for flight in flights:
            flight_coords.append(list(flight.coords))

    logger.info("Dumping coordinates to JSON string.")

    return simplejson.dumps(dict(flights=flight_coords), indent=0, ignore_nan=True)

class FlightDownloader:
    """
    Download flight data from the OpenSky impala shell using the traffic library.

    Requires traffic to be correctly configured with valid impala credentials,
    see the `traffic documentation <https://traffic-viz.github.io/opensky_impala.html>`_ for more details.

    **Summary:**

        - initialisation:
          `__init__ <#flight_processing.data.FlightDownloader.\_\_init\_\_>`_
        - downloading:
          `download_flights <#flight_processing.data.FlightDownloader.download_flights>`_,
          `save_traffic <#flight_processing.data.FlightDownloader.save_traffic>`_,
          `dump_flights <#flight_processing.data.FlightDownloader.dump_flights>`_,
          `dump_flights_bulk <#flight_processing.data.FlightDownloader.dump_flights_bulk>`_
    """

    def __init__(self, dataset):
        """
        Initialise the downloader with a given dataset.

        :param dataset: dataset name or specification
        :type dataset: str or DataConfig

        :return: object
        :rtype: FlightDownloader
        """

        if isinstance(dataset, DataConfig):
            self.__data_config = dataset
            self.dataset = dataset.dataset
        elif isinstance(dataset, str):
            logger.debug("Dataset argument {} is string, looking up known dataset.".format(dataset))
            self.__data_config = DataConfig.known_dataset(dataset)
            self.dataset = dataset
        else:
            raise ValueError("Argument 'dataset' must be of type DataConfig or str.")

    def download_flights(self, time_start, time_end, limit=None):
        """
        Download flights within the specified time interval, returning the flights as an object

        :param time_start: start time
        :type time_start: datetime.datetime or str
        :param time_end: end time
        :type time_end: datetime.datetime or str
        :param limit: maximum number of *position values* to return - note that each flight may contain thousands of position values
        :type limit: int, optional

        :return: flights
        :rtype: traffic.core.traffic.Traffic
        """

        t_start = parser.parse(str(time_start))
        t_end = parser.parse(str(time_end))
        string_start = t_start.strftime(timestring_traffic)
        string_end = t_end.strftime(timestring_traffic)

        logger.info("Downloading flights between {} and {} from OpenSky.".format(t_start, t_end))

        flights = opensky.history(
            string_start,
            string_end,
            bounds = self.__data_config.bounds_opensky,
            cached = False,
            limit = limit,
        )

        return flights

    def save_traffic(self, traffic, location):
        """
        Save the passed in flights to the specified location.

        This function is intended for the use case in which a user does not have access to the OpenSky Impala shell.
        The user can instead download traffic from another source, such as the `OpenSky REST API <https://traffic-viz.github.io/opensky_rest.html>`_,
        and save it to disk using this function.

        :param traffic: flights to save
        :type traffic: traffic.core.traffic.Traffic
        :param location: location to save the flights to
        :type location: pathlib.Path or str
        """

        out = flights_to_json(traffic)

        check_file(location)

        logger.info("Saving JSON flights to {}.".format(location))

        with open(location, "w") as outfile:
            outfile.write(out)

    def dump_flights(self, time_start, time_end):
        """
        Download flights within the specified time interval, saving the flights to a file.

        Flights will be saved to `{data_prefix}/flights/{dataset}/{date}/{time}.json`, where:
        - `data_prefix` is specified by the `DataConfig` object passed in on construction, or the `data_location` config value is used by default,
        - `dataset` is the name of the dataset as specified on construction,
        - `date` and `time` are determined by `time_start`.

        :param time_start: start time
        :type time_start: datetime.datetime or str
        :param time_end: end time
        :type time_end: datetime.datetime or str
        """

        t_start = parser.parse(str(time_start))
        t_end = parser.parse(str(time_end))

        flights = self.download_flights(t_start, t_end)

        location = self.__data_config.data_flights(t_start)

        self.save_traffic(flights, location)

    def dump_flights_bulk(self, time_start, time_end):
        """
        Download flights within the specified time interval, saving the flights to a file.

        Behaves the same as `dump_flights` but flight data is split into new files for each hour.

        :param time_start: start time
        :type time_start: datetime.datetime or str
        :param time_end: end time
        :type time_end: datetime.datetime or str
        """

        t_start = parser.parse(str(time_start))
        t_end = parser.parse(str(time_end))

        logger.info("Downloading flights in bulk between {} and {}.".format(t_start, t_end))

        execute_bulk_between(lambda t1, t2: self.dump_flights(t1, t2), t_start, t_end)
