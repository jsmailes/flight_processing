Troubleshooting
===============

I've documented some common problems/queries about this library and their potential solutions.

I'm trying to prepare my own dataset. What columns are needed in the dataframe?
-------------------------------------------------------------------------------

If importing from a file, the data must be saved as a JSON representation of a geopandas GeoDataFrame, with the following columns:

- ``name``: name of the airspace. Type ``float``.
- ``lower_limit``: lower vertical limit of the airspace, in ft. Type ``float``.
- ``upper_limit``: upper vertical limit of the airspace, in ft. Type ``float``.
- ``geometry``: lateral bounds of the airspace, given as a ``Shapely.MultiPolygon`` with coordinates in long-lat WGS84.
- ``wkt``: well-known text representation of the geometry representing the lateral bounds of the airspace. Type ``string``.

A ``geometry`` can be converted to a ``wkt`` as follows:

.. code-block:: python

    df['wkt'] = df.geometry.apply(lambda g: g.wkt)

And vice versa:

.. code-block:: python

    df['geometry'] = df.wkt.apply(shapely.wkt.loads)

A geodataframe can be saved to file as follows, using `flight_processing.DataConfig <flight_processing.DataConfig.html>`_ to get the location:

.. code-block:: python

    config = DataConfig.known_dataset("usa")
    # or: config = DataConfig("custom_name", minlon, maxlon, minlat, maxlat)
    out_location = config.dataset_location
    df.to_file(out_location, driver="GeoJSON")

If instead the dataframe is being passed into the constructor directly (only compatible with `GraphBuilder.from_dataframe <flight_processing.data.GraphBuilder.html#flight_processing.data.GraphBuilder.from_dataframe>`_ or `AirspaceGraph.__init__ <flight_processing.data.AirspaceGraph.html#flight_processing.data.AirspaceGraph.\_\_init\_\_>`_), then both pandas DataFrames and geopandas GeoDataFrames are accepted.
They require the same columns as before, but DataFrames do not need the ``geometry`` column and GeoDataFrames do not need the ``wkt`` column.


Processing data using GraphBuilder is quite slow!
-------------------------------------------------

This isn't too surprising - flight data is quite high resolution and a lot of airspaces are being checked.
It is expected that processing will take a while, especially on larger datasets or large numbers of flights.

Potential solutions include:

- Downsample the airspace geometry data stored in the saved dataframe. This can be achieved using Shapely's built-in `simplify <https://shapely.readthedocs.io/en/stable/manual.html#object.simplify>`_ method, which reduces the detail of shapes while keeping the coordinates within a certain distance of the original geometry. This will speed up airspace membership calculations without sacrificing too much accuracy.
- Run a processing script on multiple threads using ``xargs -n 1 -P <number_of_threads>``, `GNU Parallel <http://www.gnu.org/software/parallel/>`_, or a Python multithreading library..
- When preparing the dataframe of airspaces, combine rows with the same name into a single row with a single geometry. This will reduce the number of airspaces which need processing.


The confidence results returned by AirspaceGraph don't seem right!
------------------------------------------------------------------

I'm no data scientist, and the coefficients used to calculate the handover confidence were only designed to be placeholders for testing.
You should use the `set_confidence_values <flight_processing.data.AirspaceGraph.html#flight_processing.data.AirspaceGraph.set_confidence_values>`_ method to set these coefficients based on your analysis.

Alternatively you can take the values returned by `test_point <flight_processing.data.AirspaceGraph.html#flight_processing.data.AirspaceGraph.test_point>`_, `test_handover <flight_processing.data.AirspaceGraph.html#flight_processing.data.AirspaceGraph.test_handover>`_, and `test_flight <flight_processing.data.AirspaceGraph.html#flight_processing.data.AirspaceGraph.test_flight>`_, and compute your own confidence value.

Any other issues may be caused by a lack of processed data - try processing more flights.


I need more precise airspace height data.
-----------------------------------------

Currently the library assumes the airspace vertical bounds are given in the same format as the altitude of the flights being processed.
If this is not the case, or if you need to more precisely define the bounds, there are two approaches you could take:

- Split the relevant airspaces into multiple rows in the dataframe, with each row having specific vertical bounds according to your needs. Once this is done and the graph has been processed merge the relevant nodes of the graph into a single node.
- Modify the source file ``src/airspace.cpp`` and change the behaviour of ``MultiAirspace::process_flight`` or ``AirspaceBoost::inside_height`` to have the desired behaviour.


I have another question.
------------------------

If there's an issue with the library beyond what is documented here, contact me on GitHub or `create an issue <https://github.com/jsmailes/flight_processing/issues/new>`_ on the repository.