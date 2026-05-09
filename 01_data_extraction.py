import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Define and Create the Folder Architecture
folders = ["datasets", "visualizations", "scripts"]
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Directory ready: /{folder}")

ticker = "ASML"
asml = yf.Ticker(ticker)

# 2. Fetch and Route 10-Year Market Data
print(f"\nFetching 10-year market data for {ticker}...")
historical_data = asml.history(period="10y")[['Close', 'Volume']]
csv_path = os.path.join("datasets", "ASML_10yr_StockData.csv")
historical_data.to_csv(csv_path)
print(f"Saved: {csv_path}")

# Generate and Route the Graph
plt.figure(figsize=(12, 6))
plt.plot(historical_data.index, historical_data['Close'], label='ASML Close', color='#1f77b4', linewidth=1.5)
plt.title('ASML Holding N.V. - 10 Year Stock Price History', fontweight='bold')
plt.xlabel('Year')
plt.ylabel('Price (USD)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

img_path = os.path.join("visualizations", "01_ASML_10yr_Trend.png")
plt.savefig(img_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: {img_path}")

# 3. Fetch and Route Recent Financial Statements
print(f"\nFetching available financial statements...")
excel_path = os.path.join("datasets", "ASML_Financials_Incomplete.xlsx")

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    asml.financials.to_excel(writer, sheet_name='Income_Statement')
    asml.balance_sheet.to_excel(writer, sheet_name='Balance_Sheet')
    asml.cashflow.to_excel(writer, sheet_name='Cash_Flow')

print(f"Saved: {excel_path} (Ready for manual 2014-2019 data entry)")
print("\nProject setup complete! Your folders are organized.")