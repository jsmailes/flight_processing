Downloading Flights
===================

This notebook dumps flights to file using the OpenSky impala shell.
Ensure you have correctly configured the ``traffic`` library before use,
as well as setting the data location in
``~/.config/flight_processing/flight_processing.conf``.

.. code:: ipython3

    from flight_processing import DataConfig
    from flight_processing.data import FlightDownloader
    
    import logging
    
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    
    logging.getLogger('traffic').disabled = True








Example 1: known dataset
------------------------

This example uses the already encoded bounds of Switzerland to download
flights.

First we download the flights as a ``Traffic`` object, then we dump 1
hour of flights to a file, then finally we dump 3 more hours of flights
to files in a single bulk command.

.. code:: ipython3

    # Initialise downloader
    downloader = FlightDownloader("switzerland")

.. code:: ipython3

    # Download one hour of flights as a usable object
    downloader.download_flights("2020-01-01 00:00", "2020-01-01 01:00")


.. parsed-literal::

    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-01-01 00:00:00 and 2020-01-01 01:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-01-01 00:00:00+00:00 and 2020-01-01 01:00:00+00:00 and hour 2020-01-01 00:00:00+00:00 and 2020-01-01 01:00:00+00:00
    INFO:paramiko.transport:Connected (version 2.0, client OpenSSH_7.6p1)
    INFO:paramiko.transport:Authentication (password) successful!
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1577836800.0 and hour<1577840400.0 and time>=1577836800.0 and time<1577840400.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/c564afed75a09badb9ce574a5b0e280a
    INFO:numexpr.utils:Note: NumExpr detected 32 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8.
    INFO:numexpr.utils:NumExpr defaulting to 8 threads.




.. raw:: html

    <b>Traffic with 13 identifiers</b><style  type="text/css" >
    #T_f74338be_01a8_11eb_b27d_bd35c52ba63frow0_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 100.0%, transparent 100.0%);
            }#T_f74338be_01a8_11eb_b27d_bd35c52ba63frow1_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 99.9%, transparent 99.9%);
            }#T_f74338be_01a8_11eb_b27d_bd35c52ba63frow2_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 59.9%, transparent 59.9%);
            }#T_f74338be_01a8_11eb_b27d_bd35c52ba63frow3_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 44.2%, transparent 44.2%);
            }#T_f74338be_01a8_11eb_b27d_bd35c52ba63frow4_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 43.0%, transparent 43.0%);
            }#T_f74338be_01a8_11eb_b27d_bd35c52ba63frow5_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 38.5%, transparent 38.5%);
            }#T_f74338be_01a8_11eb_b27d_bd35c52ba63frow6_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 28.1%, transparent 28.1%);
            }#T_f74338be_01a8_11eb_b27d_bd35c52ba63frow7_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 16.1%, transparent 16.1%);
            }#T_f74338be_01a8_11eb_b27d_bd35c52ba63frow8_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 15.0%, transparent 15.0%);
            }#T_f74338be_01a8_11eb_b27d_bd35c52ba63frow9_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 13.1%, transparent 13.1%);
            }</style><table id="T_f74338be_01a8_11eb_b27d_bd35c52ba63f" ><thead>    <tr>        <th class="blank" ></th>        <th class="blank level0" ></th>        <th class="col_heading level0 col0" >count</th>    </tr>    <tr>        <th class="index_name level0" >icao24</th>        <th class="index_name level1" >callsign</th>        <th class="blank" ></th>    </tr></thead><tbody>
                    <tr>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel0_row0" class="row_heading level0 row0" >4b1806</th>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel1_row0" class="row_heading level1 row0" >SWR</th>
                            <td id="T_f74338be_01a8_11eb_b27d_bd35c52ba63frow0_col0" class="data row0 col0" >3599</td>
                </tr>
                <tr>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel0_row1" class="row_heading level0 row1" >4b180b</th>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel1_row1" class="row_heading level1 row1" >SWR1327</th>
                            <td id="T_f74338be_01a8_11eb_b27d_bd35c52ba63frow1_col0" class="data row1 col0" >3596</td>
                </tr>
                <tr>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel0_row2" class="row_heading level0 row2" >4b17fb</th>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel1_row2" class="row_heading level1 row2" >SWR193V</th>
                            <td id="T_f74338be_01a8_11eb_b27d_bd35c52ba63frow2_col0" class="data row2 col0" >2156</td>
                </tr>
                <tr>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel0_row3" class="row_heading level0 row3" >424352</th>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel1_row3" class="row_heading level1 row3" >AFL2605</th>
                            <td id="T_f74338be_01a8_11eb_b27d_bd35c52ba63frow3_col0" class="data row3 col0" >1591</td>
                </tr>
                <tr>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel0_row4" class="row_heading level0 row4" >3965ab</th>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel1_row4" class="row_heading level1 row4" >AFR470</th>
                            <td id="T_f74338be_01a8_11eb_b27d_bd35c52ba63frow4_col0" class="data row4 col0" >1546</td>
                </tr>
                <tr>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel0_row5" class="row_heading level0 row5" >4b5c4d</th>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel1_row5" class="row_heading level1 row5" >FLORI513</th>
                            <td id="T_f74338be_01a8_11eb_b27d_bd35c52ba63frow5_col0" class="data row5 col0" >1385</td>
                </tr>
                <tr>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel0_row6" class="row_heading level0 row6" >4b5c61</th>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel1_row6" class="row_heading level1 row6" >FLORI539</th>
                            <td id="T_f74338be_01a8_11eb_b27d_bd35c52ba63frow6_col0" class="data row6 col0" >1011</td>
                </tr>
                <tr>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel0_row7" class="row_heading level0 row7" >300621</th>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel1_row7" class="row_heading level1 row7" >IBRXA</th>
                            <td id="T_f74338be_01a8_11eb_b27d_bd35c52ba63frow7_col0" class="data row7 col0" >580</td>
                </tr>
                <tr>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel0_row8" class="row_heading level0 row8" >4b1808</th>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel1_row8" class="row_heading level1 row8" >SWR121E</th>
                            <td id="T_f74338be_01a8_11eb_b27d_bd35c52ba63frow8_col0" class="data row8 col0" >540</td>
                </tr>
                <tr>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel0_row9" class="row_heading level0 row9" >471ee2</th>
                            <th id="T_f74338be_01a8_11eb_b27d_bd35c52ba63flevel1_row9" class="row_heading level1 row9" >WZZ6192</th>
                            <td id="T_f74338be_01a8_11eb_b27d_bd35c52ba63frow9_col0" class="data row9 col0" >470</td>
                </tr>
        </tbody></table>



.. code:: ipython3

    # Download flights and dump as JSON
    downloader.dump_flights("2020-01-01 00:00", "2020-01-01 01:00")


.. parsed-literal::

    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-01-01 00:00:00 and 2020-01-01 01:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-01-01 00:00:00+00:00 and 2020-01-01 01:00:00+00:00 and hour 2020-01-01 00:00:00+00:00 and 2020-01-01 01:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1577836800.0 and hour<1577840400.0 and time>=1577836800.0 and time<1577840400.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/c564afed75a09badb9ce574a5b0e280a
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland/20200101/0000.json.


.. code:: ipython3

    # Download 3 hours of flights and dump as JSON files
    downloader.dump_flights_bulk("2020-01-01 01:00", "2020-01-01 04:00")


.. parsed-literal::

    INFO:flight_processing.data.flight_downloader:Downloading flights in bulk between 2020-01-01 01:00:00 and 2020-01-01 04:00:00.
    INFO:flight_processing.utils:Executing function 3 times between 2020-01-01 01:00:00 and 2020-01-01 04:00:00 with time delta 1:00:00.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-01-01 01:00:00 and 2020-01-01 02:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-01-01 01:00:00+00:00 and 2020-01-01 02:00:00+00:00 and hour 2020-01-01 01:00:00+00:00 and 2020-01-01 02:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1577840400.0 and hour<1577844000.0 and time>=1577840400.0 and time<1577844000.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/d64591914eb130bfebbbc8c9f09583d7
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland/20200101/0100.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-01-01 02:00:00 and 2020-01-01 03:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-01-01 02:00:00+00:00 and 2020-01-01 03:00:00+00:00 and hour 2020-01-01 02:00:00+00:00 and 2020-01-01 03:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1577844000.0 and hour<1577847600.0 and time>=1577844000.0 and time<1577847600.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/499b9720d5965dd1bcdf84191f90b274
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland/20200101/0200.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-01-01 03:00:00 and 2020-01-01 04:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-01-01 03:00:00+00:00 and 2020-01-01 04:00:00+00:00 and hour 2020-01-01 03:00:00+00:00 and 2020-01-01 04:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1577847600.0 and hour<1577851200.0 and time>=1577847600.0 and time<1577851200.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/f3e766e3c770358e6940973dc90241ff
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland/20200101/0300.json.


.. code:: ipython3

    # Cleanup
    del downloader

Example 2: new dataset
----------------------

This example manually encodes the bounds of Switzerland to download
flights in the same way as above - this can be done with any country or
region.

First we download the flights as a ``Traffic`` object, then we dump 1
hour of flights to a file, then finally we dump 23 more hours of flights
to files in a single bulk command.

.. code:: ipython3

    dataset = DataConfig("switzerland-custom", minlon=5.3, maxlon=10.7, minlat=45.5, maxlat=48, detail=6)
    downloader = FlightDownloader(dataset)

.. code:: ipython3

    # Download one hour of flights as a usable object
    downloader.download_flights("2020-03-05 00:00", "2020-03-05 01:00")


.. parsed-literal::

    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 00:00:00 and 2020-03-05 01:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 00:00:00+00:00 and 2020-03-05 01:00:00+00:00 and hour 2020-03-05 00:00:00+00:00 and 2020-03-05 01:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583366400.0 and hour<1583370000.0 and time>=1583366400.0 and time<1583370000.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/28d19cb664ef3c215b572a288db119ad




.. raw:: html

    <b>Traffic with 15 identifiers</b><style  type="text/css" >
    #T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow0_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 100.0%, transparent 100.0%);
            }#T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow1_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 76.7%, transparent 76.7%);
            }#T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow2_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 66.2%, transparent 66.2%);
            }#T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow3_col0,#T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow4_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 55.3%, transparent 55.3%);
            }#T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow5_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 46.1%, transparent 46.1%);
            }#T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow6_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 42.8%, transparent 42.8%);
            }#T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow7_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 38.9%, transparent 38.9%);
            }#T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow8_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 17.3%, transparent 17.3%);
            }#T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow9_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 15.1%, transparent 15.1%);
            }</style><table id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63f" ><thead>    <tr>        <th class="blank" ></th>        <th class="blank level0" ></th>        <th class="col_heading level0 col0" >count</th>    </tr>    <tr>        <th class="index_name level0" >icao24</th>        <th class="index_name level1" >callsign</th>        <th class="blank" ></th>    </tr></thead><tbody>
                    <tr>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel0_row0" class="row_heading level0 row0" >4b17fe</th>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel1_row0" class="row_heading level1 row0" >SWR</th>
                            <td id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow0_col0" class="data row0 col0" >3599</td>
                </tr>
                <tr>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel0_row1" class="row_heading level0 row1" >3e0a38</th>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel1_row1" class="row_heading level1 row1" >BPO245</th>
                            <td id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow1_col0" class="data row1 col0" >2761</td>
                </tr>
                <tr>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel0_row2" class="row_heading level0 row2" >4ca7f9</th>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel1_row2" class="row_heading level1 row2" >ABR1624</th>
                            <td id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow2_col0" class="data row2 col0" >2383</td>
                </tr>
                <tr>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel0_row3" class="row_heading level0 row3" >01d78d</th>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel1_row3" class="row_heading level1 row3" >ECHO2</th>
                            <td id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow3_col0" class="data row3 col0" >1991</td>
                </tr>
                <tr>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel0_row4" class="row_heading level0 row4" >44014a</th>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel1_row4" class="row_heading level1 row4" >EJU9044</th>
                            <td id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow4_col0" class="data row4 col0" >1990</td>
                </tr>
                <tr>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel0_row5" class="row_heading level0 row5" >424350</th>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel1_row5" class="row_heading level1 row5" >AFL2605</th>
                            <td id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow5_col0" class="data row5 col0" >1660</td>
                </tr>
                <tr>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel0_row6" class="row_heading level0 row6" >06a1e6</th>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel1_row6" class="row_heading level1 row6" >QTR8111</th>
                            <td id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow6_col0" class="data row6 col0" >1539</td>
                </tr>
                <tr>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel0_row7" class="row_heading level0 row7" >4caa86</th>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel1_row7" class="row_heading level1 row7" >ANE2021</th>
                            <td id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow7_col0" class="data row7 col0" >1400</td>
                </tr>
                <tr>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel0_row8" class="row_heading level0 row8" >451dbd</th>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel1_row8" class="row_heading level1 row8" >BCS130</th>
                            <td id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow8_col0" class="data row8 col0" >622</td>
                </tr>
                <tr>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel0_row9" class="row_heading level0 row9" >4b43aa</th>
                            <th id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63flevel1_row9" class="row_heading level1 row9" >RGA2</th>
                            <td id="T_007c4ac4_01a9_11eb_b27d_bd35c52ba63frow9_col0" class="data row9 col0" >545</td>
                </tr>
        </tbody></table>



.. code:: ipython3

    # Download flights and dump as JSON
    downloader.dump_flights("2020-03-05 00:00", "2020-03-05 01:00")


.. parsed-literal::

    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 00:00:00 and 2020-03-05 01:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 00:00:00+00:00 and 2020-03-05 01:00:00+00:00 and hour 2020-03-05 00:00:00+00:00 and 2020-03-05 01:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583366400.0 and hour<1583370000.0 and time>=1583366400.0 and time<1583370000.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/28d19cb664ef3c215b572a288db119ad
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0000.json.


.. code:: ipython3

    # Download 23 hours of flights and dump as JSON files
    downloader.dump_flights_bulk("2020-03-05 01:00", "2020-03-06 00:00")


.. parsed-literal::

    INFO:flight_processing.data.flight_downloader:Downloading flights in bulk between 2020-03-05 01:00:00 and 2020-03-06 00:00:00.
    INFO:flight_processing.utils:Executing function 23 times between 2020-03-05 01:00:00 and 2020-03-06 00:00:00 with time delta 1:00:00.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 01:00:00 and 2020-03-05 02:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 01:00:00+00:00 and 2020-03-05 02:00:00+00:00 and hour 2020-03-05 01:00:00+00:00 and 2020-03-05 02:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583370000.0 and hour<1583373600.0 and time>=1583370000.0 and time<1583373600.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/8e0925cfa17b75fa340f324dde14be5b
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0100.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 02:00:00 and 2020-03-05 03:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 02:00:00+00:00 and 2020-03-05 03:00:00+00:00 and hour 2020-03-05 02:00:00+00:00 and 2020-03-05 03:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583373600.0 and hour<1583377200.0 and time>=1583373600.0 and time<1583377200.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/768917fa05acf32f1b0afb2d9e8d346f
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0200.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 03:00:00 and 2020-03-05 04:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 03:00:00+00:00 and 2020-03-05 04:00:00+00:00 and hour 2020-03-05 03:00:00+00:00 and 2020-03-05 04:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583377200.0 and hour<1583380800.0 and time>=1583377200.0 and time<1583380800.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/aed113955f3719266442fb2043f6fc63
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0300.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 04:00:00 and 2020-03-05 05:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 04:00:00+00:00 and 2020-03-05 05:00:00+00:00 and hour 2020-03-05 04:00:00+00:00 and 2020-03-05 05:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583380800.0 and hour<1583384400.0 and time>=1583380800.0 and time<1583384400.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/99ec6c6a35b95a313b6037c93e0c7c16
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0400.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 05:00:00 and 2020-03-05 06:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 05:00:00+00:00 and 2020-03-05 06:00:00+00:00 and hour 2020-03-05 05:00:00+00:00 and 2020-03-05 06:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583384400.0 and hour<1583388000.0 and time>=1583384400.0 and time<1583388000.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/defdd4e424d43bcdeffda3431fcc0310
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0500.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 06:00:00 and 2020-03-05 07:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 06:00:00+00:00 and 2020-03-05 07:00:00+00:00 and hour 2020-03-05 06:00:00+00:00 and 2020-03-05 07:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583388000.0 and hour<1583391600.0 and time>=1583388000.0 and time<1583391600.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/7657b84539c72f6f617fa4f5095a1f58
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0600.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 07:00:00 and 2020-03-05 08:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 07:00:00+00:00 and 2020-03-05 08:00:00+00:00 and hour 2020-03-05 07:00:00+00:00 and 2020-03-05 08:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583391600.0 and hour<1583395200.0 and time>=1583391600.0 and time<1583395200.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/1b393565cff9a9d899b9fb460985bd31
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0700.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 08:00:00 and 2020-03-05 09:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 08:00:00+00:00 and 2020-03-05 09:00:00+00:00 and hour 2020-03-05 08:00:00+00:00 and 2020-03-05 09:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583395200.0 and hour<1583398800.0 and time>=1583395200.0 and time<1583398800.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/e7baff3622fe47dde6ce7d1ddaf4fd2a
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0800.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 09:00:00 and 2020-03-05 10:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 09:00:00+00:00 and 2020-03-05 10:00:00+00:00 and hour 2020-03-05 09:00:00+00:00 and 2020-03-05 10:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583398800.0 and hour<1583402400.0 and time>=1583398800.0 and time<1583402400.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/e64ea6e6ed69db83bda3c5cca3f6c8d8
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0900.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 10:00:00 and 2020-03-05 11:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 10:00:00+00:00 and 2020-03-05 11:00:00+00:00 and hour 2020-03-05 10:00:00+00:00 and 2020-03-05 11:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583402400.0 and hour<1583406000.0 and time>=1583402400.0 and time<1583406000.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/6ed2a01f81890dca2fdb6aedc1acd0e7
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1000.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 11:00:00 and 2020-03-05 12:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 11:00:00+00:00 and 2020-03-05 12:00:00+00:00 and hour 2020-03-05 11:00:00+00:00 and 2020-03-05 12:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583406000.0 and hour<1583409600.0 and time>=1583406000.0 and time<1583409600.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/3a94a12f2d398a9c3e44d1d35ae7b3e6
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1100.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 12:00:00 and 2020-03-05 13:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 12:00:00+00:00 and 2020-03-05 13:00:00+00:00 and hour 2020-03-05 12:00:00+00:00 and 2020-03-05 13:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583409600.0 and hour<1583413200.0 and time>=1583409600.0 and time<1583413200.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/1a7860026859e0a77453a5d0364237c8
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1200.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 13:00:00 and 2020-03-05 14:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 13:00:00+00:00 and 2020-03-05 14:00:00+00:00 and hour 2020-03-05 13:00:00+00:00 and 2020-03-05 14:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583413200.0 and hour<1583416800.0 and time>=1583413200.0 and time<1583416800.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/d5cdf044b798d884e72d3e33d67ea7e0
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1300.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 14:00:00 and 2020-03-05 15:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 14:00:00+00:00 and 2020-03-05 15:00:00+00:00 and hour 2020-03-05 14:00:00+00:00 and 2020-03-05 15:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583416800.0 and hour<1583420400.0 and time>=1583416800.0 and time<1583420400.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/156af8f9396f40c58016f78d14cb2def
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1400.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 15:00:00 and 2020-03-05 16:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 15:00:00+00:00 and 2020-03-05 16:00:00+00:00 and hour 2020-03-05 15:00:00+00:00 and 2020-03-05 16:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583420400.0 and hour<1583424000.0 and time>=1583420400.0 and time<1583424000.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/ecb8c2e81440276aabe8f4832a805c75
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1500.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 16:00:00 and 2020-03-05 17:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 16:00:00+00:00 and 2020-03-05 17:00:00+00:00 and hour 2020-03-05 16:00:00+00:00 and 2020-03-05 17:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583424000.0 and hour<1583427600.0 and time>=1583424000.0 and time<1583427600.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/c45730969ec9b83ff33c4d3eff3dc60e
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1600.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 17:00:00 and 2020-03-05 18:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 17:00:00+00:00 and 2020-03-05 18:00:00+00:00 and hour 2020-03-05 17:00:00+00:00 and 2020-03-05 18:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583427600.0 and hour<1583431200.0 and time>=1583427600.0 and time<1583431200.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/53ed8b22ff6b3044dfb091efffc627fc
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1700.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 18:00:00 and 2020-03-05 19:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 18:00:00+00:00 and 2020-03-05 19:00:00+00:00 and hour 2020-03-05 18:00:00+00:00 and 2020-03-05 19:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583431200.0 and hour<1583434800.0 and time>=1583431200.0 and time<1583434800.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/952e19914edd6e8664d84df765281b9b
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1800.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 19:00:00 and 2020-03-05 20:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 19:00:00+00:00 and 2020-03-05 20:00:00+00:00 and hour 2020-03-05 19:00:00+00:00 and 2020-03-05 20:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583434800.0 and hour<1583438400.0 and time>=1583434800.0 and time<1583438400.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/af571277f703242c929300e69b48aec8
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1900.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 20:00:00 and 2020-03-05 21:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 20:00:00+00:00 and 2020-03-05 21:00:00+00:00 and hour 2020-03-05 20:00:00+00:00 and 2020-03-05 21:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583438400.0 and hour<1583442000.0 and time>=1583438400.0 and time<1583442000.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/ad27d798c072d7639bb8dd22fd33945d
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/2000.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 21:00:00 and 2020-03-05 22:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 21:00:00+00:00 and 2020-03-05 22:00:00+00:00 and hour 2020-03-05 21:00:00+00:00 and 2020-03-05 22:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583442000.0 and hour<1583445600.0 and time>=1583442000.0 and time<1583445600.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/167c4b60aa70a23e9c114ca47df3cd12
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/2100.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 22:00:00 and 2020-03-05 23:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 22:00:00+00:00 and 2020-03-05 23:00:00+00:00 and hour 2020-03-05 22:00:00+00:00 and 2020-03-05 23:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583445600.0 and hour<1583449200.0 and time>=1583445600.0 and time<1583449200.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/3984469e45cd2eae9fec9e43f49b7865
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/2200.json.
    INFO:flight_processing.data.flight_downloader:Downloading flights between 2020-03-05 23:00:00 and 2020-03-06 00:00:00 from OpenSky.
    INFO:root:Sending request between time 2020-03-05 23:00:00+00:00 and 2020-03-06 00:00:00+00:00 and hour 2020-03-05 23:00:00+00:00 and 2020-03-06 00:00:00+00:00
    INFO:root:Sending request: select time, icao24, lat, lon, velocity, heading, vertrate, callsign, onground, alert, spi, squawk, baroaltitude, geoaltitude, lastposupdate, lastcontact, hour from state_vectors_data4  where hour>=1583449200.0 and hour<1583452800.0 and time>=1583449200.0 and time<1583452800.0 and lon>=5.3 and lon<=10.7 and lat>=45.5 and lat<=48 
    INFO:root:Reading request in cache /mnt/cold_data/josh/traffic_cache/opensky/2b540de75ee1f39ce61cba8b9f086b3c
    INFO:flight_processing.data.flight_downloader:Converting flights to list of coordinates.
    INFO:flight_processing.data.flight_downloader:Dumping coordinates to JSON string.
    INFO:flight_processing.data.flight_downloader:Saving JSON flights to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/2300.json.


.. code:: ipython3

    # Cleanup
    del downloader
