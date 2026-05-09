import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

print("Pulling data for Beta Calculation and Cash Flow Valuation...")

ticker = "ASML"
market_ticker = "^GSPC"  # S&P 500 Index used as the global market benchmark
asml = yf.Ticker(ticker)

# ==========================================
# PART 1: CALCULATING BETA (VOLATILITY RISK)
# ==========================================
# We use 5 years of monthly data, which is the Wall Street standard for Beta
asml_market = yf.download([ticker, market_ticker], period="5y", interval="1mo")['Close']

# Calculate monthly percentage returns
returns = asml_market.pct_change().dropna()

# Beta Formula: Covariance(Stock, Market) / Variance(Market)
cov_matrix = returns.cov()
cov_with_market = cov_matrix.loc[ticker, market_ticker]
market_variance = returns[market_ticker].var()
asml_beta = cov_with_market / market_variance

print(f"\n--- Risk Analysis ---")
print(f"ASML 5-Year Monthly Beta: {asml_beta:.2f}")
if asml_beta > 1:
    print("Interpretation: ASML is MORE volatile than the broader market (Aggressive Growth).")
else:
    print("Interpretation: ASML is LESS volatile than the broader market (Defensive).")

# ==========================================
# PART 2: FREE CASH FLOW (VALUATION BASIS)
# ==========================================
cash_flow = asml.cashflow

try:
    # yfinance provides Free Cash Flow directly, but we calculate it manually to show the work
    # Free Cash Flow = Operating Cash Flow - Capital Expenditures
    op_cash_flow = cash_flow.loc['Operating Cash Flow']

    # CapEx is usually reported as a negative number in cash flows, so we add it
    try:
        capex = cash_flow.loc['Capital Expenditure']
    except KeyError:
        capex = cash_flow.loc['Capital Expenditures']

    fcf = op_cash_flow + capex  # Using '+' because CapEx is already negative

    # Create DataFrame and reverse order for chronological graphing
    df_fcf = pd.DataFrame({
        'Operating Cash Flow': op_cash_flow,
        'CapEx (Reinvestment)': capex,
        'Free Cash Flow (FCF)': fcf
    }).iloc[::-1]

    print("\n--- Valuation Basis: Free Cash Flow ---")
    print(df_fcf)

    # ==========================================
    # PART 3: VISUALIZING THE CASH MACHINE
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 6))

    years = df_fcf.index.year
    width = 0.35

    # Plotting Operating Cash Flow and FCF as grouped bars
    ax.bar(years - width / 2, df_fcf['Operating Cash Flow'], width, label='Operating Cash Flow', color='#1f77b4')
    ax.bar(years + width / 2, df_fcf['Free Cash Flow (FCF)'], width, label='Free Cash Flow (FCF)', color='#2ca02c')

    # Plotting CapEx as a line to show heavy reinvestment
    ax.plot(years, abs(df_fcf['CapEx (Reinvestment)']), color='red', marker='v', linestyle='--', linewidth=2,
            label='Capital Expenditures (Absolute)')

    plt.title('ASML - Free Cash Flow Generation & Reinvestment', fontweight='bold', fontsize=14)
    plt.ylabel('Cash Value (in Billions)', fontweight='bold')
    plt.xlabel('Fiscal Year', fontweight='bold')
    plt.xticks(years)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()

    # Save Graph
    save_path = os.path.join("visualizations", "05_ASML_FreeCashFlow.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    # Save Data
    df_fcf.to_csv(os.path.join("datasets", "ASML_FCF_Valuation_Data.csv"))
    print(f"\nSuccess! FCF Valuation graph saved to {save_path}")

except KeyError as e:
    print(f"Error: API data missing row: {e}")