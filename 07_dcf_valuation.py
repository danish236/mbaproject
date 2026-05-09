import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

print("Running Discounted Cash Flow (DCF) Valuation for ASML...")

ticker = "ASML"
asml = yf.Ticker(ticker)

try:
    # 1. Gather Current Live Data
    current_price = asml.info.get('currentPrice', asml.info.get('regularMarketPrice', 900))
    shares_outstanding = asml.info.get('sharesOutstanding', 393000000)  # Fallback to approx 393M if API fails

    # Calculate recent Free Cash Flow (Using a base of ~$5.5B conservatively for projections)
    base_fcf = 5500000000

    # 2. Define DCF Assumptions (The "MBA" Inputs)
    # These are highly defensible academic estimates for a dominant tech monopoly in 2026
    revenue_growth_rate = 0.15  # 15% annual growth for the next 5 years (AI boom)
    wacc = 0.085  # 8.5% Discount Rate (Based on the Beta we calculated earlier)
    terminal_growth_rate = 0.025  # 2.5% long-term growth (Standard inflation rate)

    # 3. Project Free Cash Flows for 5 Years
    projected_fcf = []
    for year in range(1, 6):
        projected_fcf.append(base_fcf * ((1 + revenue_growth_rate) ** year))

    # 4. Calculate Terminal Value (Gordon Growth Model)
    # TV = (Year 5 FCF * (1 + Terminal Growth)) / (WACC - Terminal Growth)
    terminal_value = (projected_fcf[-1] * (1 + terminal_growth_rate)) / (wacc - terminal_growth_rate)

    # 5. Discount Everything Back to Present Value (PV)
    discounted_fcf = [fcf / ((1 + wacc) ** year) for year, fcf in enumerate(projected_fcf, 1)]
    pv_terminal_value = terminal_value / ((1 + wacc) ** 5)

    # Calculate Total Enterprise Value & Intrinsic Share Price
    enterprise_value = sum(discounted_fcf) + pv_terminal_value
    intrinsic_value_per_share = enterprise_value / shares_outstanding

    print("\n--- DCF Valuation Results ---")
    print(f"Current Trading Price: ${current_price:.2f}")
    print(f"Calculated Intrinsic Value: ${intrinsic_value_per_share:.2f}")

    if intrinsic_value_per_share > current_price:
        print("Verdict: UNDERVALUED (Stock is trading below its true cash value)")
    else:
        print("Verdict: OVERVALUED (Stock is trading at a premium due to market hype)")

    # 6. Visualize the Valuation (Current Price vs Intrinsic Value)
    plt.figure(figsize=(8, 6))
    bars = plt.bar(['Current Market Price', 'DCF Intrinsic Value'], [current_price, intrinsic_value_per_share],
                   color=['#ff7f0e', '#1f77b4'])

    plt.title('ASML - Valuation Breakdown: Market Price vs. Intrinsic Value', fontweight='bold')
    plt.ylabel('Price per Share (USD)', fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add data labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + (yval * 0.02), f'${yval:.2f}', ha='center', va='bottom',
                 fontweight='bold')

    # Save Graph
    save_path = os.path.join("visualizations", "06_ASML_DCF_Valuation.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nSuccess! DCF graph saved to {save_path}")

except Exception as e:
    print(f"Error executing DCF: {e}")