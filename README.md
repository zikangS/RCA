# RCA (Réseaux Cellulaires Avancés)
by Zi Kang Siau, Valentin Jossic, Longrui Mai & Maiwenn Kermorgant

found in https://github.com/zikangS/RCA

## Objectives and Context

This project focuses on analyzing operating cellular networks using a Universal Software Radio Peripheral (USRP) without a SIM card. All operations in this project are 100% legal and offer significant educational value in understanding cellular networks.

We will use an open-source software collection for real-time analysis of radio resources in private or commercial LTE networks called **FALCON** (Fast Analysis of LTE Control Channels).

### Project Goals
- Estimate the number of active devices connected to a targeted base station.
- Compare the performance between different operators within the same area.
- Study user habits and peak usage hours in a specific area.

### Why FALCON?
FALCON decodes the Physical Downlink Control Channel (PDCCH) of a base station, providing critical data such as:

- **Radio Network Temporary Identifiers (RNTIs)**: Unique identifiers for devices connected to a base station, allowing us to approximate the number of active and unique users over a specific time.

- **Physical Resource Block (PRB) Information**: PRB usage data helps us calculate PRB load or resource utilization by analyzing the percentage of allocated PRBs versus total available PRBs, aiding in peak utilization analysis.

## FALCON Installation
FALCON can be installed via this [link](https://github.com/falkenber9/falcon?tab=readme-ov-file#installation). You need the USRP support to make your own readings.

### Potential issues during installation

You might have a build error saying `template with C linkage`. The error is documented in [this issue](https://github.com/falkenber9/falcon/issues/8) on the falcon repository. The patch in the [second comment](https://github.com/falkenber9/falcon/issues/8#issuecomment-1761451546) solved the problem for us. Apply the patch in the source code locally and restart the compilation.

You might also get an error saying `'uint32_t' does not name a type`. Simply add `#include <stdint.h>` in the file that causes the error, and restart the compilation.

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

The **band** field is compulsory, but not the **RFCN** ones. If the RFCN is not specified, srsRAN will go over all the RFCN of the band.
Testing a large range of RFCN takes quite a long time. You can spot a specific cell by looking up the informations of the cell you are connected to with your phone. 
The RFCN (EARFCN in the case of LTE) identifies the **carrier band** and is often available in the test menu of your phone. To access it, you have to enter a code on the phone keyboard. This code depends on the manufacturer of your phone : you will have to look it up on the internet. Ultimately, you will see a list of all cells detected by your phone and their informations. Your phone is connected to the first one in the list.
Take note that the RFCN is directly linked with the band. To obtain the band your phone is connected to, you can look up an RFCN calcultor on the internet. 

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


Before running the analysis script, we highly recommend configuring your machine to fully utilize all available CPU resources to reduce processing time.

To run the analysis script:

`python3 main.py`


In this script, we trace the PRB allocation for each RNTI over time. To improve processing efficiency and produce a cleaner graph, we limit the analysis to the top 10 RNTIs with the highest PRB allocations (since base stations typically have thousands of RNTIs connected).

### Data analysis

### Maximum PRBs

We found that the maximum number of PRBs varies across different operators and base stations. This variation arises because the PRBs in a system depend on the channel bandwidth and the subcarrier spacing used in LTE or 5G NR networks.

The total number of PRBs is determined using the formula:

Number of PRBs = Channel Bandwidth (Hz) / (Subcarrier Spacing (Hz) × 12)
 
- 12 subcarriers constitute one PRB.
- Subcarrier spacing depends on the network configuration (e.g., LTE: 15 kHz, 5G: 15 kHz, 30 kHz, 60 kHz, etc.).

This formula is referenced from this [tutorial](https://www.techtrained.com/lte_prbs_calculation/)

LTE example:
|**Channel Bandwidth**   |**Number of PRBs**  |
|------------------------|--------------------|
|1.4 MHz                 |6                   |
|3 MHz                   |25                  |
|10 MHz                  |50                  |
|15 MHz                  |75                  |
|20 MHz                  |100                 |


### Constant PRB
In some cases, certain RNTIs appear to have a constant PRB value. Upon further investigation, we determined this may be due to the plotting method, where two points are connected by a straight line.

Our hypothesis is that at some point, an RNTI is allocated x PRBs, and the user disconnects. Later, another user is assigned the same RNTI and coincidentally allocated the same x PRBs. The graph connects these two points with a straight line, leading to potential confusion in the interpretation.


### RNTI distribution
At the DCI level, it is not possible to identify the exact user associated with an RNTI because we cannot link the International Mobile Equipment Identity (IMEI) to the RNTI. This creates challenges in the analysis, as we cannot confirm whether the same user consistently consumes or is allocated PRBs for a specific RNTI.
