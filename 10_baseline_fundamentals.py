import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

print("Pulling baseline financial statements and stock data for ASML...")

# Ensure visualization folder exists
os.makedirs("visualizations", exist_ok=True)

# 1. Fetch Fundamental Data
asml = yf.Ticker("ASML")
inc_stmt = asml.financials.T
bs = asml.balance_sheet.T

# Ensure data is sorted chronologically
inc_stmt = inc_stmt.sort_index()
bs = bs.sort_index()

# Extract standard columns (Handling potential missing data gracefully)
dates = inc_stmt.index.year
revenue = inc_stmt['Total Revenue'] / 1e9 if 'Total Revenue' in inc_stmt.columns else np.zeros(len(dates))
net_income = inc_stmt['Net Income'] / 1e9 if 'Net Income' in inc_stmt.columns else np.zeros(len(dates))

total_assets = bs['Total Assets'] / 1e9 if 'Total Assets' in bs.columns else np.zeros(len(dates))
total_liab = bs['Total Liabilities Net Minority Interest'] / 1e9 if 'Total Liabilities Net Minority Interest' in bs.columns else np.zeros(len(dates))
total_equity = total_assets - total_liab

# ==========================================
# GRAPH 1: Top-Line vs Bottom-Line Growth
# ==========================================
x = np.arange(len(dates))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, revenue, width, label='Total Revenue (Billions USD)', color='#1f77b4')
rects2 = ax.bar(x + width/2, net_income, width, label='Net Income (Billions USD)', color='#2ca02c')

ax.set_ylabel('Billions (USD)', fontweight='bold')
ax.set_title('ASML - Baseline Income Statement Trajectory', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(dates)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.7)

save_path_1 = os.path.join("visualizations", "11_Income_Statement_Base.png")
plt.savefig(save_path_1, dpi=300, bbox_inches='tight')
plt.close()
print(f"Success! Income Statement graph saved to {save_path_1}")

# ==========================================
# GRAPH 2: Balance Sheet Capital Structure
# ==========================================
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(dates, total_liab, label='Total Liabilities', color='#d62728')
ax.bar(dates, total_equity, bottom=total_liab, label='Shareholder Equity', color='#1f77b4')

ax.set_ylabel('Billions (USD)', fontweight='bold')
ax.set_title('ASML - Balance Sheet Capital Structure', fontweight='bold', fontsize=14)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.7)

save_path_2 = os.path.join("visualizations", "12_Balance_Sheet_Base.png")
plt.savefig(save_path_2, dpi=300, bbox_inches='tight')
plt.close()
print(f"Success! Balance Sheet graph saved to {save_path_2}")

# ==========================================
# GRAPH 3: Historical Maximum Drawdown (Risk)
# ==========================================
# Fetch 15 years of daily data to calculate drawdowns
hist = asml.history(period="15y")
hist['Peak'] = hist['Close'].cummax()
hist['Drawdown'] = (hist['Close'] - hist['Peak']) / hist['Peak'] * 100

plt.figure(figsize=(12, 5))
plt.fill_between(hist.index, hist['Drawdown'], 0, color='#d62728', alpha=0.7)
plt.title('ASML - Historical Maximum Drawdown Profile', fontweight='bold', fontsize=14)
plt.ylabel('Drawdown Percentage (%)', fontweight='bold')
plt.xlabel('Year', fontweight='bold')
plt.grid(True, linestyle=':', alpha=0.7)

save_path_3 = os.path.join("visualizations", "13_Historical_Drawdown.png")
plt.savefig(save_path_3, dpi=300, bbox_inches='tight')
plt.close()
print(f"Success! Drawdown graph saved to {save_path_3}")