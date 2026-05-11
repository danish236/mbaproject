import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

print("Generating advanced segment and ownership visualizations...")

# Ensure visualization folder exists
os.makedirs("visualizations", exist_ok=True)

# ==========================================
# GRAPH 1: Revenue Segmentation (Systems vs. Services)
# ==========================================
years = ['2019', '2020', '2021', '2022', '2023']
system_sales = np.array([8.9, 10.3, 13.6, 15.4, 21.9]) # Billions USD
service_sales = np.array([2.9, 3.6, 4.9, 5.7, 5.6])  # Billions USD

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(years, system_sales, label='Net System Sales (Hardware)', color='#1f77b4')
ax.bar(years, service_sales, bottom=system_sales, label='Installed Base Management (Services)', color='#ff7f0e')

ax.set_ylabel('Revenue (Billions USD)', fontweight='bold')
ax.set_title('ASML - Revenue Segmentation Trajectory (2019-2023)', fontweight='bold', fontsize=14)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.5)

save_path_1 = os.path.join("visualizations", "14_Revenue_Segmentation.png")
plt.savefig(save_path_1, dpi=300, bbox_inches='tight')
plt.close()
print(f"Success! Segment graph saved to {save_path_1}")

# ==========================================
# GRAPH 2: R&D Intensity (R&D as % of Revenue)
# ==========================================
rd_expenses = np.array([2.0, 2.2, 2.5, 3.3, 4.0]) # Billions USD
total_revenue = system_sales + service_sales
rd_intensity = (rd_expenses / total_revenue) * 100

plt.figure(figsize=(10, 5))
plt.plot(years, rd_intensity, marker='o', color='#d62728', linewidth=2.5, markersize=8)
plt.title('ASML - Research & Development (R&D) Intensity', fontweight='bold', fontsize=14)
plt.ylabel('R&D as % of Total Revenue', fontweight='bold')
plt.grid(True, linestyle=':', alpha=0.7)

# Annotate the exact percentages
for i, txt in enumerate(rd_intensity):
    plt.annotate(f"{txt:.1f}%", (years[i], rd_intensity[i] + 0.2), fontweight='bold')

save_path_2 = os.path.join("visualizations", "15_RD_Intensity.png")
plt.savefig(save_path_2, dpi=300, bbox_inches='tight')
plt.close()
print(f"Success! R&D Intensity graph saved to {save_path_2}")

# ==========================================
# GRAPH 3: Institutional Ownership Structure
# ==========================================
institutions = ['Capital Research', 'BlackRock', 'Baillie Gifford', 'Vanguard', 'Other Institutional', 'Retail / Public']
ownership_pct = [10.2, 7.5, 4.8, 3.5, 54.0, 20.0]
colors = ['#2ca02c', '#1f77b4', '#9467bd', '#ff7f0e', '#7f7f7f', '#d62728']

plt.figure(figsize=(10, 6))
plt.barh(institutions[::-1], ownership_pct[::-1], color=colors[::-1])
plt.title('ASML - Estimated Equity Ownership Structure (2024)', fontweight='bold', fontsize=14)
plt.xlabel('Percentage of Outstanding Shares (%)', fontweight='bold')
plt.grid(axis='x', linestyle='--', alpha=0.5)

# Annotate percentages
for index, value in enumerate(ownership_pct[::-1]):
    plt.text(value + 0.5, index, f"{value}%", va='center', fontweight='bold')

save_path_3 = os.path.join("visualizations", "16_Ownership_Structure.png")
plt.savefig(save_path_3, dpi=300, bbox_inches='tight')
plt.close()
print(f"Success! Ownership graph saved to {save_path_3}")