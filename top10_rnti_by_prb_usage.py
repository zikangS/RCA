import pandas as pd
import matplotlib.pyplot as plt

COLUMNS_FALCON_DCI = [
    'timestamp', 'sfn', 'subframe', 'rnti', 'direction', 'mcs_idx', 
    'nof_prb', 'tbs_sum', 'tbs_0', 'tbs_1', 'format', 'ndi', 'ndi_1', 
    'harq_idx', 'ncce', 'L', 'cfi', 'histval', 'nof_bits', 'hex'
]

data = pd.read_csv(
    'falconeye_capture_2162.4.csv',
    sep='\t', 
    names=COLUMNS_FALCON_DCI
)

#for data with header and seperated by comma
'''
data = pd.read_csv(
    'falconeye_capture_2162.4.csv',
    sep=',', 
    names=COLUMNS_FALCON_DCI,
    dtype={
        'timestamp': 'float64', 
        'sfn': 'int64', 
        'subframe': 'int64', 
        'rnti': 'str',  # Keep RNTI as string
        'direction': 'int64', 
        'nof_prb': 'int64', 
        'tbs_sum': 'int64'
    }, 
    skiprows=1,  # Skip the first row header
    low_memory=False
)
'''

# Group by RNTI and calculate total PRB usage
prb_usage = data.groupby('rnti')['nof_prb'].sum()

# Show only the top 10 RNTIs by PRB usage
top_n = 10
prb_usage_top = prb_usage.sort_values(ascending=False).head(top_n)

plt.figure(figsize=(12, 6))
prb_usage_top.plot(kind='bar', color='blue')
plt.title(f'Top {top_n} RNTIs by PRB Usage')
plt.xlabel('RNTI')
plt.ylabel('Total PRBs Allocated')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()
