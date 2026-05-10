import pandas as pd
import matplotlib.pyplot as plt
import os

print("Generating extra market visualizations from 10-year dataset...")

# Load the existing dataset
file_path = os.path.join("datasets", "ASML_10yr_StockData.csv")
df = pd.read_csv(file_path)

# FIX: Explicitly convert the 'Date' column to proper datetime objects, handling the timezone offset
df['Date'] = pd.to_datetime(df['Date'], utc=True)
df.set_index('Date', inplace=True)
df.index = df.index.tz_localize(None)

# ---------------------------------------------------------
# Graph 1: Institutional Accumulation (Monthly Volume)
# ---------------------------------------------------------
# Resample daily volume to monthly volume
monthly_volume = df['Volume'].resample('ME').sum()

plt.figure(figsize=(12, 6))
plt.bar(monthly_volume.index, monthly_volume.values / 1e6, color='#2ca02c', alpha=0.7, width=20)
plt.title('ASML - Institutional Accumulation (Monthly Trading Volume)', fontweight='bold', fontsize=14)
plt.ylabel('Total Volume (in Millions)', fontweight='bold')
plt.xlabel('Year', fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Save Graph 1
save_path_1 = os.path.join("visualizations", "07_ASML_Trading_Volume.png")
plt.savefig(save_path_1, dpi=300, bbox_inches='tight')
plt.close()
print(f"Success! Volume graph saved to {save_path_1}")

# ---------------------------------------------------------
# Graph 2: Macroeconomic Volatility (30-Day Rolling Risk)
# ---------------------------------------------------------
df['Daily Return'] = df['Close'].pct_change()
df['Rolling Volatility'] = df['Daily Return'].rolling(window=30).std() * 100

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Rolling Volatility'], color='#d62728', linewidth=1.5)

# Highlight the COVID-19 / Supply Chain shock period
plt.axvspan(pd.to_datetime('2020-02-01'), pd.to_datetime('2021-06-01'), color='gray', alpha=0.2, label='Pandemic Supply Chain Shock')

plt.title('ASML - 30-Day Rolling Volatility (Systematic Risk Assessment)', fontweight='bold', fontsize=14)
plt.ylabel('Volatility (%)', fontweight='bold')
plt.xlabel('Year', fontweight='bold')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)

# Save Graph 2
save_path_2 = os.path.join("visualizations", "08_ASML_Rolling_Volatility.png")
plt.savefig(save_path_2, dpi=300, bbox_inches='tight')
plt.close()
print(f"Success! Volatility graph saved to {save_path_2}")