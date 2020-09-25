Installation
============

This library has a number of dependencies, most notably the `traffic <https://github.com/xoolive/traffic>`_ library, for which you can find installation instructions `here <https://traffic-viz.github.io/installation.html>`_.

The library also relies on `scipy <https://www.scipy.org/>`_ and `numpy <https://numpy.org/>`_ for data types and mathematical functions, and `pandas <https://pandas.pydata.org/>`_, `geopandas <https://geopandas.org/>`_, and `Shapely <https://pypi.org/project/Shapely/>`_ for processing airspace data.

Visualisations are provided through `matplotlib <https://matplotlib.org/>`_, `cartopy <https://scitools.org.uk/cartopy/docs/latest/>`_, `pyproj <https://github.com/pyproj4/pyproj>`_, and `hvplot <https://hvplot.holoviz.org/>`_. The `simplejson <https://simplejson.readthedocs.io/en/latest/>`_ library enables data exporting, and `networkx <https://networkx.github.io/>`_ is used to build directed graphs.

.. warning::
   Certain dependencies (particularly `cartopy` and `shapely`) require access to libraries which may not be present on the system. The `Anaconda <https://www.anaconda.com/distribution/#download-section>`_ platform is much better at handling these dependencies - if possible, install it first then run the following:

   .. parsed-literal::
      conda install cartopy shapely
      pip install flight_processing

   Additional dependencies can also be installed using Anaconda if desired.

Installation using pip
----------------------

The package is available on `PyPI <https://pypi.org/>`_ and can be installed as follows:

.. parsed-literal::
   pip install flight_processing

Manual build and installation
------------------------------

We can also build and install the package manually using python's ``setuptools``.

Install prerequisites
~~~~~~~~~~~~~~~~~~~~~

Building the package requires a number of prerequisites, both to compile the C++ component and to install the python library itself.

First install the following using your package manager:

.. code-block:: none

   git
   cmake
   gcc-c++
   python3
   boost-devel
   boost-python3-devel
   boost-numpy3

.. note::
   The above package names are correct on Fedora Linux, but they may differ depending on your operating system. The following package names can be used on Ubuntu:

   .. code-block:: none

      git
      cmake
      g++
      python3-dev
      libboost-all-dev

Next we need to install some python prerequisites:

.. parsed-literal::
   pip install setuptools wheel

Clone repository
~~~~~~~~~~~~~~~~

Now we clone the repository from Github:

.. parsed-literal::
   git clone --recurse-submodules https://github.com/jsmailes/flight_processing
   cd flight_processing

Build wheel (optional)
~~~~~~~~~~~~~~~~~~~~~~

To build a wheel and/or source tarball using ``setuptools``, run the following:

.. parsed-literal::
   python3 setup.py sdist bdist_wheel

These can then be installed using ``pip`` if desired.

Install
~~~~~~~

Installation is fairly straightforward, since ``pip`` installs the prerequisites and runs ``setup.py`` for us:

.. parsed-literal::
   pip install .

Troubleshooting
~~~~~~~~~~~~~~~

Issues with python dependencies can usually be fixed by installing them using `Anaconda <https://www.anaconda.com/distribution/#download-section>`_.

Cryptic issues with CMake are usually caused by having an incorrect version of Python and/or Boost installed.

If you're having any more problems, please `create an issue <https://github.com/jsmailes/flight_processing/issues>`_ on the Github repo with some details about your system and the problem you're having.