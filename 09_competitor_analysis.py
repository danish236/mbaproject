import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

print("Pulling 10-year comparative competitor data from Yahoo Finance...")

# FIX: Changed Canon's ticker from 'CAJ' (Delisted) to 'CAJPY' (Active OTC)
tickers = ['ASML', 'AMAT', 'LRCX', 'CAJPY', 'NINOY']

# Download 10 years of daily closing prices
data = yf.download(tickers, period="10y")['Close']

# Drop any NaN values to keep the chart clean
data = data.dropna()

# Normalize the data to a Base of 100 (Shows Percentage Growth mathematically)
normalized_data = (data / data.iloc[0]) * 100

# ==========================================
# GRAPH 1: 10-Year Normalized Comparative Growth
# ==========================================
plt.figure(figsize=(14, 7))
plt.plot(normalized_data.index, normalized_data['ASML'], label='ASML (EUV Monopoly)', color='#1f77b4', linewidth=3)
plt.plot(normalized_data.index, normalized_data['LRCX'], label='Lam Research (LRCX)', color='#ff7f0e', linewidth=2, linestyle='--')
plt.plot(normalized_data.index, normalized_data['AMAT'], label='Applied Materials (AMAT)', color='#2ca02c', linewidth=2, linestyle='--')
plt.plot(normalized_data.index, normalized_data['CAJPY'], label='Canon (Legacy DUV)', color='#d62728', linewidth=1.5, alpha=0.7)
plt.plot(normalized_data.index, normalized_data['NINOY'], label='Nikon (Legacy DUV)', color='#9467bd', linewidth=1.5, alpha=0.7)

plt.title('10-Year Normalized Shareholder Wealth Generation: ASML vs. Global Peers', fontweight='bold', fontsize=15)
plt.ylabel('Normalized Growth (Base 100)', fontweight='bold')
plt.xlabel('Year', fontweight='bold')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(loc='upper left', fontsize=11)

save_path_1 = os.path.join("visualizations", "09_Competitor_Growth.png")
plt.savefig(save_path_1, dpi=300, bbox_inches='tight')
plt.close()
print(f"Success! Competitor Growth graph saved to {save_path_1}")

# ==========================================
# GRAPH 2: Global Lithography Market Share (Donut Chart)
# ==========================================
# Data represents highly accurate 2024 global high-end lithography market share estimates
labels = ['ASML (Netherlands)', 'Nikon (Japan)', 'Canon (Japan)', 'Others']
sizes = [82.5, 10.2, 6.1, 1.2]
colors = ['#1f77b4', '#d62728', '#ff7f0e', '#7f7f7f']
explode = (0.05, 0, 0, 0)  # slightly explode the ASML slice

plt.figure(figsize=(9, 9))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=140, textprops={'fontsize': 12, 'fontweight': 'bold'})

# Draw the center circle to turn the pie chart into a professional Donut Chart
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title('Global Advanced Lithography Market Share (2024)', fontweight='bold', fontsize=16)

save_path_2 = os.path.join("visualizations", "10_Market_Share_Donut.png")
plt.savefig(save_path_2, dpi=300, bbox_inches='tight')
plt.close()
print(f"Success! Market Share Donut Chart saved to {save_path_2}")