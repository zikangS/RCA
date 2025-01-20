import pandas
import matplotlib.pyplot as plt
from mplcursors import cursor
import pltinteractivelegend
from datetime import datetime

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

# data = pandas.read_csv('falconeye_capture_2162.4.csv', sep='\t', names=COLUMNS_FALCON_DCI)
data = pandas.read_csv('falconeye_capture_1870_1850_21_100_4_RNTi7063.csv', sep=',', names=COLUMNS_FALCON_DCI, skiprows=1, low_memory=False)  #for data with header and seperated by comma
# print(data)

timestamps = data['timestamp'].tolist()
unique_RNTI = data['rnti'].unique()

print(unique_RNTI.shape)

RNTI_prb = []
col_filter = ['timestamp', 'rnti', 'nof_prb', 'tbs_sum']

data = data[col_filter]

prb_usage = data.groupby('rnti')['nof_prb'].sum()

# Show only the top 10 RNTIs by PRB usage
top_n = 10
prb_usage_top = prb_usage.sort_values(ascending=False).head(top_n)

data = data.loc[data['rnti'].isin(prb_usage_top.index)]
data['date'] = [datetime.fromtimestamp(d) for d in data['timestamp']]

print(prb_usage_top.index)
print(data)

fig, ax = plt.subplots(figsize=(8,6))

data.groupby('rnti').plot(x='date', y='nof_prb', ax=ax, kind='line', style='.-')

plt.legend(prb_usage_top.index, bbox_to_anchor=(1.04, 1), loc="upper left", ncol=2)
plt.title('prb vs time')
leg = pltinteractivelegend.InteractiveLegend()

cursor()
plt.show()