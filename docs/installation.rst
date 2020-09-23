Installation
============

This library has a number of dependencies, most notably the `traffic <https://github.com/xoolive/traffic>`_ library, for which you can find installation instructions `here <https://traffic-viz.github.io/installation.html>`_.

The library also relies on `scipy <https://www.scipy.org/>`_ and `numpy <https://numpy.org/>`_ for data types and mathematical functions, and `pandas <https://pandas.pydata.org/>`_, `geopandas <https://geopandas.org/>`_, and `Shapely <https://pypi.org/project/Shapely/>`_ for processing airspace data.

Visualisations are provided through `matplotlib <https://matplotlib.org/>`_, `cartopy <https://scitools.org.uk/cartopy/docs/latest/>`_, `pyproj <https://github.com/pyproj4/pyproj>`_, and `hvplot <https://hvplot.holoviz.org/>`_. The `simplejson <https://simplejson.readthedocs.io/en/latest/>`_ library enables data exporting, and `networkx <https://networkx.github.io/>`_ is used to build directed graphs.

Pip should handle the installation of these dependencies, allowing the following two installation options:

.. parsed-literal::
   git clone https://github.com/jsmailes/flight_processing
   cd flight_processing
   pip install .

.. parsed-literal::
   pip install flight_processing

.. warning::
   Certain dependencies (particularly `cartopy` and `shapely`) require access to libraries which may not be present on the system. The `Anaconda <https://www.anaconda.com/distribution/#download-section>`_ platform is much better at handling these dependencies - if possible, install it first then do the following:

   .. parsed-literal::
      conda install cartopy shapely
      pip install flight_processing

   Additional dependencies can also be installed using Anaconda if desired.
