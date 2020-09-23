Core Structure
==============

The library is based around three classes for data handling and processing, and one helper class:

- airspace bounds and other parameters are specified using `flight_processing.DataConfig <flight_processing.DataConfig.html>`_,
- flights are downloaded through `flight_processing.data.FlightDownloader <flight_processing.data.FlightDownloader.html>`_,
- a graph of airspace handovers is produced using `flight_processing.data.GraphBuilder <flight_processing.data.GraphBuilder.html>`_,
- and finally the resulting graph is visualised and used for further processing in `flight_processing.data.AirspaceGraph <flight_processing.data.AirspaceGraph.html>`_.

Each of the ``data`` classes contain an underlying `geopandas GeoDataFrame <https://geopandas.org/>`_, and ``GraphBuilder`` and ``AirspaceGraph`` make use of an underlying C++ class (``AirspaceHandler``) for faster and more efficient processing.

The ``FlightDownloader`` class uses Xavier Olive's `traffic <https://traffic-viz.github.io/index.html>`_ library to download flights from the `OpenSky Network <https://opensky-network.org/>`_.

**Contents**

.. toctree::
    :maxdepth: 1

    flight_processing.DataConfig
    flight_processing.data.FlightDownloader
    flight_processing.data.GraphBuilder
    flight_processing.data.AirspaceGraph
