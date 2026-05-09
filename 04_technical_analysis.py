import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

print("Pulling 15 years of market data for ASML...")

# 1. Fetch 15 years of daily stock data
ticker = "ASML"
asml = yf.Ticker(ticker)
hist = asml.history(period="15y")

# 2. Calculate Technical Indicators
# 50-day Simple Moving Average (Short term momentum)
hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
# 200-day Simple Moving Average (Long term trend)
hist['SMA_200'] = hist['Close'].rolling(window=200).mean()

# 3. Calculate 15-Year CAGR (Compound Annual Growth Rate)
start_price = hist['Close'].iloc[0]
end_price = hist['Close'].iloc[-1]
years = 15
cagr = ((end_price / start_price) ** (1 / years)) - 1

print(f"\n--- 15-Year Performance Metrics ---")
print(f"Starting Price (15 yrs ago): ${start_price:.2f}")
print(f"Current Price: ${end_price:.2f}")
print(f"15-Year CAGR: {cagr * 100:.2f}%")

# 4. Visualize the Technical Analysis
plt.figure(figsize=(14, 7))

plt.plot(hist.index, hist['Close'], label='ASML Close Price', color='black', alpha=0.6, linewidth=1)
plt.plot(hist.index, hist['SMA_50'], label='50-Day Moving Average', color='blue', linewidth=1.5)
plt.plot(hist.index, hist['SMA_200'], label='200-Day Moving Average', color='red', linewidth=2)

# Formatting the graph for the MBA paper
plt.title(f'ASML 15-Year Technical Analysis & Moving Averages (CAGR: {cagr * 100:.1f}%)', fontweight='bold', fontsize=14)
plt.ylabel('Stock Price (USD)', fontweight='bold')
plt.xlabel('Year', fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper left')

# Save to visualizations folder
save_path = os.path.join("visualizations", "03_ASML_Technical_15yr.png")
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"\nSuccess! Technical analysis graph saved to {save_path}")

# Save the dataset
data_path = os.path.join("datasets", "ASML_15yr_Technical_Data.csv")
hist.to_csv(data_path)