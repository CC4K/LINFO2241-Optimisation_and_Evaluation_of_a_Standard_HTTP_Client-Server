import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns

df = pd.read_csv('measurements/test_case_CUDA.csv')

order = ['normal', 'best', '4', '8', '16', '32']

settings_map = {
    'normal': 'Normal',
    'best': 'Best',
    '4': 'Block Size 4',
    '8': 'Block Size 8',
    '16': 'Block Size 16',
    '32': 'Block Size 32',
}

df['Settings'] = pd.Categorical(df['Settings'], categories=order, ordered=True)

df['Settings'] = df['Settings'].map(settings_map)

grouped = df.groupby('Settings', observed=True)['Requests/sec'].agg(['mean', 'std']).reset_index()

positions = range(len(grouped))

colors = ['#ff7f0e' if setting == 'CUDA Optimized' else '#1f77b4' if setting in ['Normal', 'Best'] else '#76b900' for setting in grouped['Settings']]

plt.figure(figsize=(10, 6))
plt.grid(True, axis='y', which='both', zorder=1)
bars = plt.bar(positions, grouped['mean'], yerr=grouped['std'], color=colors, alpha=1, capsize=5, zorder=2)

plt.xlabel('Configuration', fontsize=14)
plt.ylabel('Requests/sec', fontsize=14)
plt.title('Performance vs Configuration', fontsize=14)
# plt.yscale('log')
plt.xticks(positions, grouped['Settings'])

legend_handles = [
    Patch(facecolor='#1f77b4', edgecolor='black', label='Non-CUDA (Normal, Best)'),
    Patch(facecolor='#76b900', edgecolor='black', label='CUDA Block Size'),
]
plt.legend(handles=legend_handles)

# plt.show()
plt.savefig('graph.png')