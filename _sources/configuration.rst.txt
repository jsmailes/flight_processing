Configuration
=============

Before we get started we need to correctly configure the library.

This library will save quite a few large files to disk (downloaded flights, processed graphs) and it needs a folder to do so. By default this folder will be python's current directory, but it can be set to a specific folder by modifying the config file (located by default at ``~/.config/flight_processing/flight_processing.conf``):

.. code-block:: none

   [global]
   data_location = /path/to/data/dir

We must also configure the `traffic <https://traffic-viz.github.io/index.html>`_ library so it uses correct credentials for the `OpenSky <https://opensky-network.org/>`_ Impala interface. More detailed documentation can be found `here <https://traffic-viz.github.io/opensky_impala.html>`, but the gist is as follows:

Edit the following lines in your traffic configuration file:

.. code-block:: none

   [opensky]
   username =
   password =
