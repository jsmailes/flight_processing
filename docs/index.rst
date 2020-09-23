.. Flight Processing documentation master file, created by
   sphinx-quickstart on Mon Sep 21 17:24:33 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

flight_processing
=================

Source code on `GitHub <https://github.com/jsmailes/flight_processing>`_.

This library is aimed at extracting useful information from historical flight data and airspace data. It uses Xavier Olive's `Traffic <https://github.com/xoolive/traffic>`_ library to download flights from the `OpenSky Network <https://opensky-network.org/>`_'s Impala shell as well as importing airspace data from GeoPandas dataframes.

Explicit functionality is provided to download flights in bulk (dumping to files), process flights into a directed graph of airspace handovers, and test specific points/handovers/flights against a graph to provide a confidence score.
Where explicit functionality is not provided, access is given to the underlying data structure for direct manipulation.

Improvements and bug fixes are welcome, simply submit a pull request on GitHub.

.. toctree::
   :maxdepth: 1

   installation
   quickstart
   core_structure


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
