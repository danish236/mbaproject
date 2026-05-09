import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

print("Pulling fundamental risk data for ASML...")

ticker = "ASML"
asml = yf.Ticker(ticker)

inc_stmt = asml.financials
bal_sheet = asml.balance_sheet

try:
    # 1. Extracting the Data (handling yfinance naming variations)
    revenue = inc_stmt.loc['Total Revenue']
    gross_profit = inc_stmt.loc['Gross Profit']

    current_assets = bal_sheet.loc['Current Assets']
    current_liabilities = bal_sheet.loc['Current Liabilities']

    total_debt = bal_sheet.loc['Total Debt']

    try:
        total_equity = bal_sheet.loc['Stockholders Equity']
    except KeyError:
        total_equity = bal_sheet.loc['Total Stockholder Equity']

    # 2. Building the DataFrame (Reverse order so oldest is first)
    df = pd.DataFrame({
        'Revenue': revenue,
        'Gross Profit': gross_profit,
        'Current Assets': current_assets,
        'Current Liabilities': current_liabilities,
        'Total Debt': total_debt,
        'Total Equity': total_equity
    }).iloc[::-1]

    # 3. Calculating the MBA Financial Metrics
    df['Gross Margin (%)'] = (df['Gross Profit'] / df['Revenue']) * 100
    df['Current Ratio (Liquidity)'] = df['Current Assets'] / df['Current Liabilities']
    df['Debt-to-Equity (Solvency)'] = df['Total Debt'] / df['Total Equity']

    print("\n--- 4-Year Fundamental Risk Metrics ---")
    print(df[['Gross Margin (%)', 'Current Ratio (Liquidity)', 'Debt-to-Equity (Solvency)']])

    # 4. Visualizing the Risk Profile (Dual-Axis Chart)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Axis 1: Ratios (Lines)
    ax1.set_xlabel('Fiscal Year', fontweight='bold')
    ax1.set_ylabel('Ratio Multiplier', color='black', fontweight='bold')
    line1 = ax1.plot(df.index.year, df['Current Ratio (Liquidity)'], marker='o', color='blue',
                     label='Current Ratio (Target > 1.0)')
    line2 = ax1.plot(df.index.year, df['Debt-to-Equity (Solvency)'], marker='s', color='red', linestyle='--',
                     label='Debt-to-Equity')
    ax1.tick_params(axis='y', labelcolor='black')

    # Axis 2: Gross Margin (Bars)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Gross Margin (%)', color='green', fontweight='bold')
    bar1 = ax2.bar(df.index.year, df['Gross Margin (%)'], alpha=0.2, color='green', width=0.4, label='Gross Margin (%)')
    ax2.tick_params(axis='y', labelcolor='green')
    # Set y-axis limit slightly higher so bars don't overlap lines too much
    ax2.set_ylim(0, df['Gross Margin (%)'].max() * 1.5)

    # Title and Legend
    plt.title('ASML - Corporate Liquidity, Solvency, & Margin Profile', fontweight='bold', fontsize=14)
    ax1.set_xticks(df.index.year)

    # Combine legends from both axes
    lines = line1 + line2 + [bar1]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    # Save Graph
    save_path = os.path.join("visualizations", "04_ASML_Risk_Profile.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    # Save Data
    df.to_csv(os.path.join("datasets", "ASML_Fundamental_Risk_Data.csv"))
    print(f"\nSuccess! Risk analysis graph saved to {save_path}")

except KeyError as e:
    print(f"Error: API data structure missing row: {e}")