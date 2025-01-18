# RCA (Réseaux Cellulaires Avancés)

## Objectives and Context

This project focuses on analyzing operating cellular networks using a Universal Software Radio Peripheral (USRP) without a SIM card. All operations in this project are 100% legal and offer significant educational value in understanding cellular networks.

We will use an open-source software collection for real-time analysis of radio resources in private or commercial LTE networks called **FALCON** (Fast Analysis of LTE Control Channels). It can be installed via this [link](https://github.com/falkenber9/falcon).

### Project Goals
- Estimate the number of active devices connected to a targeted base station.
- Compare the performance between different operators within the same area.
- Study user habits and peak usage hours in a specific area.

### Why FALCON?
FALCON decodes the Physical Downlink Control Channel (PDCCH) of a base station, providing critical data such as:

- **Radio Network Temporary Identifiers (RNTIs)**: Unique identifiers for devices connected to a base station, allowing us to approximate the number of active and unique users over a specific time.

- **Physical Resource Block (PRB) Information**: PRB usage data helps us calculate PRB load or resource utilization by analyzing the percentage of allocated PRBs versus total available PRBs, aiding in peak utilization analysis.




## Real-Time Monitoring
### Using FALCON GUI

To monitor a targeted base station with FALCON, three main parameters are required:
- Cell ID
- PRB (Physical Resource Block)
- Frequency

These parameters can be obtained using the **srsRAN** software. Once srsRAN is installed, connect the USRP to your machine and use the [`cell_search`](https://github.com/srsran/srsRAN_4G/blob/master/lib/examples/cell_search.c) tool:

Command:

`./srsLTE-build/lib/examples/cell_search -b <band> -s <start of RFCN> -e <end of RFCN>`

Expected output:

`Found CELL <freq> MHz, EARFCN = <earfcn>, PHYID = <cell id>, <prb> PRB, <ports> ports, PSS power = <power> dBm`

After obtaining the **Cell ID**, **PRB**, and **Frequency**, enter these parameters into the FALCON GUI and click **Start**. The program will begin processing, displaying graphs of the data.

**Note**: If the signal strength is weak, multiple attempts may be needed to display the data successfully.


### Using terminal
Monitoring multiple operators and timeframes manually via the GUI is time-consuming. FALCON provides a command-line option, allowing for automated scripting to handle multiple operators and timestamps.

Command:

`./FalconEye -f <freq in MHz>e6 -n <time of the record in ms> - D <location of the file saved>`

The detailed Downlink Control Information (DCI) captured will be saved as a CSV file containing the following columns :

|**Column**   |**Description**                                                            |
|-------------|---------------------------------------------------------------------------|
|timestamp    |unix timestamp in [s] as float, 1µs resolution                             |
|sfn          |system frame number                                                        |
|subframe     |subframe index {0,1,...,9}                                                 |
|rnti         |the addressed RNTI                                                         |
|direction    |0 for uplink alloc., 1 for downlink alloc.                                 |
|mcs_idx      |MCS index of the first transport block                                     |
|nof_prb      |number of allocated PRBs                                                   |
|tbs_sum      |total Transport Block Size (TBS) in [Bit]                                  |
|tbs_0        |TBS of first transport block (-1 for SISO)                                 |
|tbs_1        |TBS of second transport block (-1 for SISO)                                |
|format       |index+1 of DCI format in array flacon_ue_all_formats[], see DCISearch.cc   |
|ndi          |new data indicator for first transport block                               |
|ndi_1        |new data indicator for second transport block                              |
|harq_idx     |HARQ index                                                                 |
|ncce         |index of first Control Channel Element (CCE) of this DCI within PDCCH      |
|L            |aggregation level of this DCI {0..3}, occupies 2^L consecutive CCEs.       |
|cfi          |number of OFDM symbols occupied by PDCCH                                   |
|histval      |number of occurences of this RNTI within last 200ms                        |
|nof_bits     |DCI length (without CRC)                                                   |
|hex          |raw DCI content as hex string, see sscan_hex()/sprint_hex() in falcon_dci.c|




## Data Presentation

After obtaining the data, install required dependencies:

`pip install -r requirements.txt`

Run the analysis script:

`python3 main.py`

**Note**: The interactive legend feature is currently unavailable for both plots.




