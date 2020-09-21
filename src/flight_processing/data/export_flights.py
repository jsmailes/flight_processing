from ..utils import DataConfig, check_file, execute_bulk, execute_bulk_between

from datetime import timedelta
from dateutil import parser

from traffic.data import opensky
import simplejson

import sys

timestring_traffic = "%Y-%m-%d %H:%M"

def flights_to_json(flights):
    flight_coords = []

    if flights is not None:
        for flight in flights:
            flight_coords.append(list(flight.coords))

    return simplejson.dumps(dict(flights=flight_coords), indent=0, ignore_nan=True)

class FlightDownloader:
    def __init__(self, dataset, verbose=False):
        if isinstance(dataset, DataConfig):
            self.__data_config = dataset
            self.dataset = dataset.dataset
        elif isinstance(dataset, str):
            self.__data_config = DataConfig.known_dataset(dataset)
            self.dataset = dataset
        else:
            raise ValueError("Argument 'dataset' must be of type DataConfig or str.")

        self.verbose = verbose

    def download_flights(self, time_start, time_end, limit=None):
        t_start = parser.parse(str(time_start))
        t_end = parser.parse(str(time_end))
        string_start = t_start.strftime(timestring_traffic)
        string_end = t_end.strftime(timestring_traffic)

        flights = opensky.history(
            string_start,
            string_end,
            bounds = self.__data_config.bounds_opensky,
            cached = False,
            limit = limit,
        )

        return flights

    def dump_flights(self, time_start, time_end):
        t_start = parser.parse(str(time_start))
        t_end = parser.parse(str(time_end))

        if self.verbose:
            print("Downloading flights from {} to {}.".format(t_start, t_end))

        flights = self.download_flights(t_start, t_end)

        if self.verbose:
            print("Converting to JSON.")

        out = flights_to_json(flights)

        location = self.__data_config.data_flights(t_start)
        check_file(location)

        if self.verbose:
            print("Saving to {}.".format(location))

        with open(location, "w") as outfile:
            outfile.write(out)

    def dump_flights_bulk(self, time_start, time_end):
        t_start = parser.parse(str(time_start))
        t_end = parser.parse(str(time_end))

        execute_bulk_between(lambda t1, t2: self.dump_flights(t1, t2), t_start, t_end)