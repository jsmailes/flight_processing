Importing the USA’s Airspaces
=============================

We import data on the USA’s airspaces from `a dataset provided by the
FAA <https://adds-faa.opendata.arcgis.com/datasets/c6a62360338e408cb1512366ad61559e_0>`__.
This data already contains all the information we need so it requires
very little processing.

Setup
-----

.. code:: ipython3

    import requests
    from datetime import datetime, timezone
    import time
    import numpy as np
    import pandas as pd
    import descartes, geopandas
    from shapely.geometry import LineString, Point, Polygon, MultiPolygon, base
    from shapely.ops import transform
    
    import math
    import matplotlib.pyplot as plt
    
    import cartopy.crs as ccrs
    import cartopy.geodesic as cgeo
    import cartopy.io.img_tiles as cimgt
    import cartopy.feature as cfeature

Initial Data Processing
-----------------------

We download the file using a built-in geopandas method, and do some
basic processing to get the geometry and vertical limits into formats
that the rest of the processing code can work with.

.. code:: ipython3

    url = "https://opendata.arcgis.com/datasets/c6a62360338e408cb1512366ad61559e_0.geojson"
    gdf = geopandas.read_file(url)

NOTE: as it turns out the z-coordinate is completely unused so
``vertical_limits`` is unnecessary. I’m leaving it here in case it comes
in handy later.

.. code:: ipython3

    def vertical_limits(geom):
        def _limits_from_coords(c):
            l = list(map(lambda t: t[2], list(c)))
            return (min(l), max(l))
        
        if isinstance(geom, Polygon):
            return _limits_from_coords(geom.exterior.coords)
        elif isinstance(geom, MultiPolygon):
            lims = list(map(list, zip(*[ _limits_from_coords(g.exterior.coords) for g in geom ])))
            return (min(lims[0]), max(lims[1]))
        else:
            raise NotImplementedError

.. code:: ipython3

    def process_geometry(shape):
        shape2 = transform(lambda x, y, z: tuple(filter(None, [x, y])), shape).buffer(0)
        if isinstance(shape2, Polygon):
            return MultiPolygon([shape2])
        elif isinstance(shape2, MultiPolygon):
            return shape2
        else:
            raise NotImplementedError
    
    def process_vertical_limits(upper, upper_units, lower, lower_units):
        if upper_units == "FT":
            upper_ft = int(upper)
        elif upper_units == "FL":
            upper_ft = int(upper) * 100
        else:
            upper_ft = 1000000 # Assume 'None' is unrestricted, this should be large enough
        if upper_ft < 0:
            upper_ft = 1000000 # See above
        
        if lower_units == "FT":
            lower_ft = int(lower)
        elif lower_units == "FL":
            lower_ft = int(lower) * 100
        else:
            lower_ft = 0 # Assume 'None' is unrestricted, return ground level
        return (upper_ft, lower_ft)
    
    gdf['geometry'] = gdf.geometry.apply(process_geometry)
    gdf['upper_limit'], gdf['lower_limit'] = zip(*gdf.apply(lambda row: process_vertical_limits(row.UPPER_VAL, row.UPPER_UOM, row.LOWER_VAL, row.LOWER_UOM), axis=1))
    gdf['name'] = gdf['NAME']
    del gdf['NAME']
    gdf




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>OBJECTID</th>
          <th>GLOBAL_ID</th>
          <th>IDENT</th>
          <th>ICAO_ID</th>
          <th>UPPER_DESC</th>
          <th>UPPER_VAL</th>
          <th>UPPER_UOM</th>
          <th>UPPER_CODE</th>
          <th>LOWER_DESC</th>
          <th>LOWER_VAL</th>
          <th>...</th>
          <th>AK_LOW</th>
          <th>US_LOW</th>
          <th>US_AREA</th>
          <th>PACIFIC</th>
          <th>Shape__Area</th>
          <th>Shape__Length</th>
          <th>geometry</th>
          <th>upper_limit</th>
          <th>lower_limit</th>
          <th>name</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>2AC361E6-08A9-49E8-8B3B-AA68EE41363C</td>
          <td>CZYZ</td>
          <td>CZYZ</td>
          <td>TI</td>
          <td>17999</td>
          <td>FT</td>
          <td>MSL</td>
          <td>None</td>
          <td>4500</td>
          <td>...</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1.655436</td>
          <td>7.583659</td>
          <td>MULTIPOLYGON (((-81.20495 44.50579, -81.20936 ...</td>
          <td>17999</td>
          <td>4500</td>
          <td>TORONTO, ON CAE 8</td>
        </tr>
        <tr>
          <th>1</th>
          <td>2</td>
          <td>3B2EA57E-2618-47A3-BC52-DF07A2DB6F97</td>
          <td>CZWG</td>
          <td>CZWG</td>
          <td>TI</td>
          <td>17999</td>
          <td>FT</td>
          <td>MSL</td>
          <td>None</td>
          <td>12501</td>
          <td>...</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>4.581230</td>
          <td>8.016952</td>
          <td>MULTIPOLYGON (((-95.96780 49.79961, -95.96764 ...</td>
          <td>17999</td>
          <td>12501</td>
          <td>KENORA, ON CAE</td>
        </tr>
        <tr>
          <th>2</th>
          <td>3</td>
          <td>E229E560-CA7D-45A7-AFD6-9FF3E01113C6</td>
          <td>CZVR</td>
          <td>CZVR</td>
          <td>TI</td>
          <td>12500</td>
          <td>FT</td>
          <td>MSL</td>
          <td>None</td>
          <td>2000</td>
          <td>...</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0.074797</td>
          <td>1.798322</td>
          <td>MULTIPOLYGON (((-122.55477 49.10081, -122.5547...</td>
          <td>12500</td>
          <td>2000</td>
          <td>PITT MEADOWS CAE</td>
        </tr>
        <tr>
          <th>3</th>
          <td>4</td>
          <td>7099FA1B-406E-4896-BA81-F74E30AECFCE</td>
          <td>CZVR</td>
          <td>CZVR</td>
          <td>TI</td>
          <td>6500</td>
          <td>FT</td>
          <td>MSL</td>
          <td>None</td>
          <td>3200</td>
          <td>...</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0.016077</td>
          <td>0.598732</td>
          <td>MULTIPOLYGON (((-123.50967 49.37969, -123.5091...</td>
          <td>6500</td>
          <td>3200</td>
          <td>VANCOUVER, BC TCA</td>
        </tr>
        <tr>
          <th>4</th>
          <td>5</td>
          <td>7FD391DB-1145-44CF-A32F-64B192FA284E</td>
          <td>CZYZ</td>
          <td>CZYZ</td>
          <td>TI</td>
          <td>3300</td>
          <td>FT</td>
          <td>MSL</td>
          <td>None</td>
          <td>0</td>
          <td>...</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0.030340</td>
          <td>0.630070</td>
          <td>MULTIPOLYGON (((-76.71478 44.22523, -76.71477 ...</td>
          <td>3300</td>
          <td>0</td>
          <td>KINGSTON, ON CTLZ</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>5794</th>
          <td>5795</td>
          <td>C471BE9C-6BBD-4DB6-8809-490E740EA021</td>
          <td>NOW</td>
          <td>KNOW</td>
          <td>TI</td>
          <td>2500</td>
          <td>FT</td>
          <td>MSL</td>
          <td>None</td>
          <td>0</td>
          <td>...</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0.002927</td>
          <td>0.197640</td>
          <td>MULTIPOLYGON (((-123.41226 48.11634, -123.4149...</td>
          <td>2500</td>
          <td>0</td>
          <td>PORT ANGELES CGAS CLASS E2</td>
        </tr>
        <tr>
          <th>5795</th>
          <td>5796</td>
          <td>4DCDB3FC-9149-4A58-B040-7F668E971B5D</td>
          <td>NOW</td>
          <td>KNOW</td>
          <td>AA</td>
          <td>-9998</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>0</td>
          <td>...</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0.008285</td>
          <td>0.475549</td>
          <td>MULTIPOLYGON (((-123.39775 48.11881, -123.3968...</td>
          <td>1000000</td>
          <td>0</td>
          <td>PORT ANGELES CGAS CLASS E4</td>
        </tr>
        <tr>
          <th>5796</th>
          <td>5797</td>
          <td>D76D7CA4-4715-4991-AD59-DF1A7003A3EA</td>
          <td>None</td>
          <td>None</td>
          <td>AA</td>
          <td>-9998</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>700</td>
          <td>...</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0.049059</td>
          <td>0.895362</td>
          <td>MULTIPOLYGON (((-124.52673 42.55188, -124.4869...</td>
          <td>1000000</td>
          <td>700</td>
          <td>GOLD BEACH CLASS E5</td>
        </tr>
        <tr>
          <th>5797</th>
          <td>5798</td>
          <td>F9D11D29-3001-4E66-A8C5-62BF1232E64B</td>
          <td>None</td>
          <td>None</td>
          <td>AA</td>
          <td>-9998</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>1200</td>
          <td>...</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0.262581</td>
          <td>1.855594</td>
          <td>MULTIPOLYGON (((-124.42158 42.16528, -124.4240...</td>
          <td>1000000</td>
          <td>1200</td>
          <td>GOLD BEACH CLASS E5</td>
        </tr>
        <tr>
          <th>5798</th>
          <td>5799</td>
          <td>ECDCC2C9-DC4D-41A9-B17B-81C0D52FE798</td>
          <td>None</td>
          <td>None</td>
          <td>AA</td>
          <td>-9998</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>700</td>
          <td>...</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0.034226</td>
          <td>0.855681</td>
          <td>MULTIPOLYGON (((-123.52795 48.22726, -123.2646...</td>
          <td>1000000</td>
          <td>700</td>
          <td>PORT ANGELES CGAS CLASS E5</td>
        </tr>
      </tbody>
    </table>
    <p>5799 rows × 42 columns</p>
    </div>



Visualising Airspaces
---------------------

We can now plot the airspaces on a map.

.. code:: ipython3

    fig = plt.figure(dpi=300, figsize=(7,7))
    
    imagery = cimgt.Stamen(style="terrain-background")
    ax = plt.axes(projection=imagery.crs)
    
    minlon = -130
    maxlon = -58
    minlat = 23
    maxlat = 46
    
    ax.set_extent((minlon, maxlon, minlat, maxlat))
    ax.add_image(imagery, 4)
    
    ax.add_geometries(gdf.geometry, crs=ccrs.PlateCarree(), facecolor="none", edgecolor="black")
    
    ax.set_aspect('auto')
    
    plt.show()



.. image:: airspace_data_usa_files/airspace_data_usa_9_0.png


Export Data
-----------

We save the data to a file.

.. code:: ipython3

    from flight_processing import DataConfig

.. code:: ipython3

    config = DataConfig.known_dataset("usa")
    out_location = config.dataset_location
    out_location




.. parsed-literal::

    '/mnt/cold_data/josh/processing/regions_usa_wkt.json'



.. code:: ipython3

    gdf_out = gdf.copy()
    
    gdf_out['wkt'] = gdf_out.geometry.apply(lambda g: g.wkt)
    
    gdf_out.to_file(out_location, driver="GeoJSON")
    
    del gdf_out
