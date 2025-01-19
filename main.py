import pandas
import matplotlib.pyplot as plt
from mplcursors import cursor
import pltinteractivelegend

COLUMNS_FALCON_DCI = [
    'timestamp',    # unix timestamp in [s] as float, 1µs resolution
    'sfn',          # system frame number
    'subframe',     # subframe index {0,1,...,9}
    'rnti',         # the addressed RNTI
    'direction',    # 0 for uplink alloc., 1 for downlink alloc.
    'mcs_idx',      # MCS index of the first transport block
    'nof_prb',      # number of allocated PRBs
    'tbs_sum',      # total Transport Block Size (TBS) in [Bit]
    'tbs_0',        # TBS of first transport block (-1 for SISO)
    'tbs_1',        # TBS of second transport block (-1 for SISO)
    'format',       # index+1 of DCI format in array flacon_ue_all_formats[], see DCISearch.cc
    'ndi',          # new data indicator for first transport block
    'ndi_1',        # new data indicator for second transport block
    'harq_idx',     # HARQ index
    'ncce',         # index of first Control Channel Element (CCE) of this DCI within PDCCH
    'L',            # aggregation level of this DCI {0..3}, occupies 2^L consecutive CCEs.
    'cfi',          # number of OFDM symbols occupied by PDCCH
    'histval',      # number of occurences of this RNTI within last 200ms
    'nof_bits',     # DCI length (without CRC)
    'hex'           # raw DCI content as hex string, see sscan_hex()/sprint_hex() in falcon_dci.c 
]

data = pandas.read_csv('falconeye_capture_2162.4.csv', sep='\t', names=COLUMNS_FALCON_DCI)
#data = pandas.read_csv('try_data.csv', sep=',', names=COLUMNS_FALCON_DCI, skiprows=1, low_memory=False)  #for data with header
print(data)

timestamps = data['timestamp'].tolist()
unique_RNTI = data['rnti'].unique()

RNTI_prb = []
col_filter = ['timestamp', 'rnti', 'nof_prb', 'tbs_sum']

for rnti in unique_RNTI:
    df = data[data['rnti'] == rnti]
    df = df[col_filter]
    for index in list(data.index.values):
        if index in df.index:
            continue
        df.loc[index] = timestamps[index], rnti, 0, 0
    df = df.sort_index()
    RNTI_prb.append(df)

for df in RNTI_prb:
    plt.plot(timestamps, df['nof_prb'].tolist(), label=df['rnti'][0])
plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", ncol=2)
plt.title('prb vs time')
leg = pltinteractivelegend.InteractiveLegend()

plt.figure()
for df in RNTI_prb:
    plt.plot(timestamps, df['tbs_sum'].tolist(), label=df['rnti'][0])
plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", ncol=2)
plt.title('tbs vs time')
leg = pltinteractivelegend.InteractiveLegend()

cursor()
plt.show()