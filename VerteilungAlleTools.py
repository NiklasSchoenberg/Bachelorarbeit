import re
import matplotlib.pyplot as plt
import math
import numpy as np
from collections import Counter

tools = 9

with open('KommentareToolScores.csv', 'r') as file:
    lines = file.readlines()

header = lines[0].strip().split(',')

data = [line.strip().split(',') for line in lines[1:]]

header = header[-tools:]
data = [row[-tools:] for row in data]

num_charts = len(header)

fig, axes = plt.subplots(math.ceil(math.sqrt(tools)), math.ceil(math.sqrt(tools)), figsize=(20, 10))
axes = axes.flatten()

for col_idx in range(num_charts):
    col_values = []
    for row in data[-100:]:
        try:
            col_values.append(float(row[col_idx]))
        except ValueError:
            continue
    
    bins = np.arange(-1, 1.01, 0.1)
    col_values_binned = np.digitize(col_values, bins) - 1
    frequency_count = Counter(col_values_binned)
    
    x_values = bins[:-1] + 0.05
    y_frequency = [frequency_count[i] for i in range(len(bins)-1)]
    
    axes[col_idx].bar(x_values, y_frequency, width=0.1, align='center')
    
    axes[col_idx].set_xlabel('Polarity-Scores')
    axes[col_idx].set_ylabel('Häufigkeit')
    
    axes[col_idx].set_title(header[col_idx])
    
    axes[col_idx].set_ylim(0, max(y_frequency, default=1))

plt.tight_layout()
plt.show()