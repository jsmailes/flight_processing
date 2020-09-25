Downloading Flights
===================

This notebook dumps flights to file using the OpenSky impala shell.
Ensure you have correctly configured the ``traffic`` library before use,
as well as setting the data location in
``~/.config/flight_processing/flight_processing.conf``.

.. code:: ipython3

    from flight_processing import DataConfig
    from flight_processing.data import FlightDownloader








Example 1: known dataset
------------------------

This example uses the already encoded bounds of Switzerland to download
flights.

First we download the flights as a ``Traffic`` object, then we dump 1
hour of flights to a file, then finally we dump 3 more hours of flights
to files in a single bulk command.

.. code:: ipython3

    # Initialise downloader
    downloader = FlightDownloader("switzerland", verbose=True)

.. code:: ipython3

    # Download one hour of flights as a usable object
    downloader.download_flights("2020-01-01 00:00", "2020-01-01 01:00")




.. raw:: html

    <b>Traffic with 13 identifiers</b><style  type="text/css" >
    #T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow0_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 100.0%, transparent 100.0%);
            }#T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow1_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 99.9%, transparent 99.9%);
            }#T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow2_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 59.9%, transparent 59.9%);
            }#T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow3_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 44.2%, transparent 44.2%);
            }#T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow4_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 43.0%, transparent 43.0%);
            }#T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow5_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 38.5%, transparent 38.5%);
            }#T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow6_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 28.1%, transparent 28.1%);
            }#T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow7_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 16.1%, transparent 16.1%);
            }#T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow8_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 15.0%, transparent 15.0%);
            }#T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow9_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 13.1%, transparent 13.1%);
            }</style><table id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5b" ><thead>    <tr>        <th class="blank" ></th>        <th class="blank level0" ></th>        <th class="col_heading level0 col0" >count</th>    </tr>    <tr>        <th class="index_name level0" >icao24</th>        <th class="index_name level1" >callsign</th>        <th class="blank" ></th>    </tr></thead><tbody>
                    <tr>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel0_row0" class="row_heading level0 row0" >4b1806</th>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel1_row0" class="row_heading level1 row0" >SWR</th>
                            <td id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow0_col0" class="data row0 col0" >3599</td>
                </tr>
                <tr>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel0_row1" class="row_heading level0 row1" >4b180b</th>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel1_row1" class="row_heading level1 row1" >SWR1327</th>
                            <td id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow1_col0" class="data row1 col0" >3596</td>
                </tr>
                <tr>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel0_row2" class="row_heading level0 row2" >4b17fb</th>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel1_row2" class="row_heading level1 row2" >SWR193V</th>
                            <td id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow2_col0" class="data row2 col0" >2156</td>
                </tr>
                <tr>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel0_row3" class="row_heading level0 row3" >424352</th>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel1_row3" class="row_heading level1 row3" >AFL2605</th>
                            <td id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow3_col0" class="data row3 col0" >1591</td>
                </tr>
                <tr>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel0_row4" class="row_heading level0 row4" >3965ab</th>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel1_row4" class="row_heading level1 row4" >AFR470</th>
                            <td id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow4_col0" class="data row4 col0" >1546</td>
                </tr>
                <tr>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel0_row5" class="row_heading level0 row5" >4b5c4d</th>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel1_row5" class="row_heading level1 row5" >FLORI513</th>
                            <td id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow5_col0" class="data row5 col0" >1385</td>
                </tr>
                <tr>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel0_row6" class="row_heading level0 row6" >4b5c61</th>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel1_row6" class="row_heading level1 row6" >FLORI539</th>
                            <td id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow6_col0" class="data row6 col0" >1011</td>
                </tr>
                <tr>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel0_row7" class="row_heading level0 row7" >300621</th>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel1_row7" class="row_heading level1 row7" >IBRXA</th>
                            <td id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow7_col0" class="data row7 col0" >580</td>
                </tr>
                <tr>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel0_row8" class="row_heading level0 row8" >4b1808</th>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel1_row8" class="row_heading level1 row8" >SWR121E</th>
                            <td id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow8_col0" class="data row8 col0" >540</td>
                </tr>
                <tr>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel0_row9" class="row_heading level0 row9" >471ee2</th>
                            <th id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5blevel1_row9" class="row_heading level1 row9" >WZZ6192</th>
                            <td id="T_bdf9eb5c_fd8e_11ea_8882_a33c5ff21b5brow9_col0" class="data row9 col0" >470</td>
                </tr>
        </tbody></table>



.. code:: ipython3

    # Download flights and dump as JSON
    downloader.dump_flights("2020-01-01 00:00", "2020-01-01 01:00")


.. parsed-literal::

    Downloading flights from 2020-01-01 00:00:00 to 2020-01-01 01:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland/20200101/0000.json.


.. code:: ipython3

    # Download 3 hours of flights and dump as JSON files
    downloader.dump_flights_bulk("2020-01-01 01:00", "2020-01-01 04:00")


.. parsed-literal::

    Downloading flights from 2020-01-01 01:00:00 to 2020-01-01 02:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland/20200101/0100.json.
    Downloading flights from 2020-01-01 02:00:00 to 2020-01-01 03:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland/20200101/0200.json.
    Downloading flights from 2020-01-01 03:00:00 to 2020-01-01 04:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland/20200101/0300.json.


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
    downloader = FlightDownloader(dataset, verbose=True)

.. code:: ipython3

    # Download one hour of flights as a usable object
    downloader.download_flights("2020-03-05 00:00", "2020-03-05 01:00")




.. raw:: html

    <b>Traffic with 15 identifiers</b><style  type="text/css" >
    #T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow0_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 100.0%, transparent 100.0%);
            }#T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow1_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 76.7%, transparent 76.7%);
            }#T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow2_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 66.2%, transparent 66.2%);
            }#T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow3_col0,#T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow4_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 55.3%, transparent 55.3%);
            }#T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow5_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 46.1%, transparent 46.1%);
            }#T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow6_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 42.8%, transparent 42.8%);
            }#T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow7_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 38.9%, transparent 38.9%);
            }#T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow8_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 17.3%, transparent 17.3%);
            }#T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow9_col0{
                width:  10em;
                 height:  80%;
                background:  linear-gradient(90deg,#5fba7d 15.1%, transparent 15.1%);
            }</style><table id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5b" ><thead>    <tr>        <th class="blank" ></th>        <th class="blank level0" ></th>        <th class="col_heading level0 col0" >count</th>    </tr>    <tr>        <th class="index_name level0" >icao24</th>        <th class="index_name level1" >callsign</th>        <th class="blank" ></th>    </tr></thead><tbody>
                    <tr>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel0_row0" class="row_heading level0 row0" >4b17fe</th>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel1_row0" class="row_heading level1 row0" >SWR</th>
                            <td id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow0_col0" class="data row0 col0" >3599</td>
                </tr>
                <tr>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel0_row1" class="row_heading level0 row1" >3e0a38</th>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel1_row1" class="row_heading level1 row1" >BPO245</th>
                            <td id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow1_col0" class="data row1 col0" >2761</td>
                </tr>
                <tr>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel0_row2" class="row_heading level0 row2" >4ca7f9</th>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel1_row2" class="row_heading level1 row2" >ABR1624</th>
                            <td id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow2_col0" class="data row2 col0" >2383</td>
                </tr>
                <tr>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel0_row3" class="row_heading level0 row3" >01d78d</th>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel1_row3" class="row_heading level1 row3" >ECHO2</th>
                            <td id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow3_col0" class="data row3 col0" >1991</td>
                </tr>
                <tr>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel0_row4" class="row_heading level0 row4" >44014a</th>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel1_row4" class="row_heading level1 row4" >EJU9044</th>
                            <td id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow4_col0" class="data row4 col0" >1990</td>
                </tr>
                <tr>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel0_row5" class="row_heading level0 row5" >424350</th>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel1_row5" class="row_heading level1 row5" >AFL2605</th>
                            <td id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow5_col0" class="data row5 col0" >1660</td>
                </tr>
                <tr>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel0_row6" class="row_heading level0 row6" >06a1e6</th>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel1_row6" class="row_heading level1 row6" >QTR8111</th>
                            <td id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow6_col0" class="data row6 col0" >1539</td>
                </tr>
                <tr>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel0_row7" class="row_heading level0 row7" >4caa86</th>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel1_row7" class="row_heading level1 row7" >ANE2021</th>
                            <td id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow7_col0" class="data row7 col0" >1400</td>
                </tr>
                <tr>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel0_row8" class="row_heading level0 row8" >451dbd</th>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel1_row8" class="row_heading level1 row8" >BCS130</th>
                            <td id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow8_col0" class="data row8 col0" >622</td>
                </tr>
                <tr>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel0_row9" class="row_heading level0 row9" >4b43aa</th>
                            <th id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5blevel1_row9" class="row_heading level1 row9" >RGA2</th>
                            <td id="T_cbaa4e04_fd8e_11ea_8882_a33c5ff21b5brow9_col0" class="data row9 col0" >545</td>
                </tr>
        </tbody></table>



.. code:: ipython3

    # Download flights and dump as JSON
    downloader.dump_flights("2020-03-05 00:00", "2020-03-05 01:00")


.. parsed-literal::

    Downloading flights from 2020-03-05 00:00:00 to 2020-03-05 01:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0000.json.


.. code:: ipython3

    # Download 23 hours of flights and dump as JSON files
    downloader.dump_flights_bulk("2020-03-05 01:00", "2020-03-06 00:00")


.. parsed-literal::

    Downloading flights from 2020-03-05 01:00:00 to 2020-03-05 02:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0100.json.
    Downloading flights from 2020-03-05 02:00:00 to 2020-03-05 03:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0200.json.
    Downloading flights from 2020-03-05 03:00:00 to 2020-03-05 04:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0300.json.
    Downloading flights from 2020-03-05 04:00:00 to 2020-03-05 05:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0400.json.
    Downloading flights from 2020-03-05 05:00:00 to 2020-03-05 06:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0500.json.
    Downloading flights from 2020-03-05 06:00:00 to 2020-03-05 07:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0600.json.
    Downloading flights from 2020-03-05 07:00:00 to 2020-03-05 08:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0700.json.
    Downloading flights from 2020-03-05 08:00:00 to 2020-03-05 09:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0800.json.
    Downloading flights from 2020-03-05 09:00:00 to 2020-03-05 10:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/0900.json.
    Downloading flights from 2020-03-05 10:00:00 to 2020-03-05 11:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1000.json.
    Downloading flights from 2020-03-05 11:00:00 to 2020-03-05 12:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1100.json.
    Downloading flights from 2020-03-05 12:00:00 to 2020-03-05 13:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1200.json.
    Downloading flights from 2020-03-05 13:00:00 to 2020-03-05 14:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1300.json.
    Downloading flights from 2020-03-05 14:00:00 to 2020-03-05 15:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1400.json.
    Downloading flights from 2020-03-05 15:00:00 to 2020-03-05 16:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1500.json.
    Downloading flights from 2020-03-05 16:00:00 to 2020-03-05 17:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1600.json.
    Downloading flights from 2020-03-05 17:00:00 to 2020-03-05 18:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1700.json.
    Downloading flights from 2020-03-05 18:00:00 to 2020-03-05 19:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1800.json.
    Downloading flights from 2020-03-05 19:00:00 to 2020-03-05 20:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/1900.json.
    Downloading flights from 2020-03-05 20:00:00 to 2020-03-05 21:00:00.
    Converting to JSON.
    Saving to /mnt/cold_data/josh/processing/flights/switzerland-custom/20200305/2000.json.
    Downloading flights from 2020-03-05 21:00:00 to 2020-03-05 22:00:00.


.. code:: ipython3

    # Cleanup
    del downloader
