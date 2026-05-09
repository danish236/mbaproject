import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

print("Pulling clean financial data from API...")

# 1. Fetch data
ticker = "ASML"
asml = yf.Ticker(ticker)

# Get financials (Income Statement) and balance sheet
inc_stmt = asml.financials
bal_sheet = asml.balance_sheet

# 2. Extract the exact metrics we need for DuPont Analysis
# We use try/except to gracefully handle any missing rows
try:
    # yfinance returns data with most recent year first (leftmost column)
    revenue = inc_stmt.loc['Total Revenue']
    net_income = inc_stmt.loc['Net Income']
    total_assets = bal_sheet.loc['Total Assets']

    # Equity can sometimes be named differently in yfinance depending on the company
    try:
        total_equity = bal_sheet.loc['Stockholders Equity']
    except KeyError:
        total_equity = bal_sheet.loc['Total Stockholder Equity']

    # 3. Create a clean DataFrame (and reverse order so oldest year is first)
    df = pd.DataFrame({
        'Revenue': revenue,
        'Net Income': net_income,
        'Total Assets': total_assets,
        'Total Equity': total_equity
    }).iloc[::-1]  # Reverses the rows for chronological order

    # 4. Calculate DuPont Components
    df['Profit Margin'] = df['Net Income'] / df['Revenue']
    df['Asset Turnover'] = df['Revenue'] / df['Total Assets']
    df['Equity Multiplier'] = df['Total Assets'] / df['Total Equity']
    df['ROE'] = df['Profit Margin'] * df['Asset Turnover'] * df['Equity Multiplier']

    print("\n--- DuPont Analysis Results ---")
    print(df[['Profit Margin', 'Asset Turnover', 'Equity Multiplier', 'ROE']])

    # 5. Visualize the ROE Trend
    plt.figure(figsize=(10, 6))

    # Plotting the three components
    plt.plot(df.index.year, df['ROE'] * 100, marker='o', color='black', linewidth=3, label='ROE (%)')
    plt.plot(df.index.year, df['Profit Margin'] * 100, marker='s', color='blue', linestyle='--',
             label='Profit Margin (%)')

    plt.title('ASML - DuPont Analysis: Drivers of Return on Equity', fontweight='bold', fontsize=14)
    plt.ylabel('Percentage (%)', fontweight='bold')
    plt.xlabel('Fiscal Year', fontweight='bold')

    # Ensure x-axis only shows whole years
    plt.xticks(df.index.year)

    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()

    # Save the graph
    save_path = os.path.join("visualizations", "02_ASML_DuPont.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\nSuccess! DuPont graph generated and saved to {save_path}")

    # Save the clean data to CSV for your records
    data_path = os.path.join("datasets", "ASML_Clean_DuPont_Data.csv")
    df.to_csv(data_path)

except KeyError as e:
    print(f"Error: API data structure changed. Missing row: {e}")