"""
generate_static_dashboard.py
Creates an executive-level static dashboard using Matplotlib.
Outputs:
- ecommerce_dashboard.png (High-resolution 300 DPI image)
- ecommerce_dashboard.pdf (Print/submission-ready vector PDF)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec

def build_dashboard(clean_csv_path, output_dir):
    print("Generating executive static dashboard...")
    df = pd.read_csv(clean_csv_path)
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])

    # Overall KPIs
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100
    total_units = df['Quantity'].sum()
    avg_order_value = total_sales / df['Order_ID'].nunique()

    # Style configuration
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['axes.edgecolor'] = '#CBD5E1'
    plt.rcParams['axes.linewidth'] = 0.8

    # Canvas Setup: 20 x 14 inches
    fig = plt.figure(figsize=(20, 14), facecolor='#F1F5F9')
    
    # GridSpec layout:
    # Row 0: Header Banner (title, subtitle, meta)
    # Row 1: 5 KPI Metric Cards
    # Row 2-3: Charts (2x3 or custom grid)
    gs = GridSpec(4, 3, figure=fig, height_ratios=[0.8, 0.9, 3.8, 3.8], 
                  hspace=0.35, wspace=0.25, left=0.04, right=0.96, top=0.96, bottom=0.04)

    # -------------------------------------------------------------
    # 1. HEADER BANNER
    # -------------------------------------------------------------
    ax_header = fig.add_subplot(gs[0, :])
    ax_header.axis('off')
    
    # Background rounded container for header
    header_box = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.03",
                                        facecolor="#0F172A", edgecolor="none", transform=ax_header.transAxes)
    ax_header.add_patch(header_box)
    
    ax_header.text(0.02, 0.65, "EXECUTIVE E-COMMERCE & RETAIL PERFORMANCE DASHBOARD",
                   color="#FFFFFF", fontsize=20, fontweight='bold', va='center', transform=ax_header.transAxes)
    ax_header.text(0.02, 0.28, "Global Sales, Profit Margins, Regional Demographics & Fulfillment Logistics (2024 - 2025)",
                   color="#94A3B8", fontsize=11, va='center', transform=ax_header.transAxes)
    ax_header.text(0.98, 0.48, "Report Period: 24 Months | 2,500 Transactions\nData Status: Cleaned & Validated",
                   color="#38BDF8", fontsize=10, fontweight='medium', ha='right', va='center', transform=ax_header.transAxes)

    # -------------------------------------------------------------
    # 2. KPI METRIC CARDS (5 cards in Row 1)
    # -------------------------------------------------------------
    kpis = [
        {"title": "TOTAL REVENUE", "value": f"${total_sales:,.0f}", "sub": "Gross Net Revenue", "color": "#2563EB", "bg": "#EFF6FF"},
        {"title": "TOTAL PROFIT", "value": f"${total_profit:,.0f}", "sub": "Operating Net Income", "color": "#059669", "bg": "#ECFDF5"},
        {"title": "PROFIT MARGIN", "value": f"{profit_margin:.1f}%", "sub": "Target: >12.0%", "color": "#0D9488", "bg": "#F0FDFA"},
        {"title": "UNITS SOLD", "value": f"{total_units:,}", "sub": "2,500 Completed Orders", "color": "#D97706", "bg": "#FFFBEB"},
        {"title": "AVG ORDER VALUE", "value": f"${avg_order_value:.2f}", "sub": "Revenue Per Basket", "color": "#7C3AED", "bg": "#F5F3FF"}
    ]

    gs_kpi = gs[1, :].subgridspec(1, 5, wspace=0.15)
    for i, kpi in enumerate(kpis):
        ax_kpi = fig.add_subplot(gs_kpi[0, i])
        ax_kpi.axis('off')
        card = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.03,rounding_size=0.06",
                                      facecolor="#FFFFFF", edgecolor="#E2E8F0", linewidth=1.2, transform=ax_kpi.transAxes)
        ax_kpi.add_patch(card)
        # Left colored accent line
        accent = patches.Rectangle((0, 0.15), 0.03, 0.7, facecolor=kpi["color"], edgecolor="none", transform=ax_kpi.transAxes)
        ax_kpi.add_patch(accent)

        ax_kpi.text(0.08, 0.72, kpi["title"], color="#64748B", fontsize=9, fontweight='bold', transform=ax_kpi.transAxes)
        ax_kpi.text(0.08, 0.40, kpi["value"], color="#0F172A", fontsize=17, fontweight='bold', transform=ax_kpi.transAxes)
        ax_kpi.text(0.08, 0.18, kpi["sub"], color=kpi["color"], fontsize=8.5, fontweight='semibold', transform=ax_kpi.transAxes)

    # -------------------------------------------------------------
    # 3. CHART 1: MONTHLY SALES & PROFIT TREND (Row 2, Cols 0-1 spanning 2 columns)
    # -------------------------------------------------------------
    ax1 = fig.add_subplot(gs[2, :2])
    ax1.set_facecolor('#FFFFFF')
    
    monthly = df.groupby('Year_Month').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    monthly['Year_Month_Dt'] = pd.to_datetime(monthly['Year_Month'])
    monthly = monthly.sort_values('Year_Month_Dt')

    x_labels = monthly['Year_Month'].tolist()
    x_indices = np.arange(len(x_labels))

    ax1.plot(x_indices, monthly['Sales'], color='#2563EB', linewidth=2.5, marker='o', markersize=4.5, label='Monthly Sales ($)')
    ax1.fill_between(x_indices, monthly['Sales'], color='#3B82F6', alpha=0.12)
    ax1.plot(x_indices, monthly['Profit'], color='#10B981', linewidth=2.2, linestyle='--', marker='s', markersize=4, label='Monthly Profit ($)')

    ax1.set_title("1. Monthly Revenue & Operating Profit Trajectory (2024 - 2025)", fontsize=12, fontweight='bold', color='#1E293B', pad=12, loc='left')
    ax1.set_xticks(x_indices)
    ax1.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8, color='#475569')
    ax1.set_ylabel("Amount ($ USD)", fontsize=9.5, fontweight='bold', color='#475569')
    ax1.yaxis.set_major_formatter('${x:,.0f}')
    ax1.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax1.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#E2E8F0', fontsize=8.5, loc='upper left')

    # Add peak callout
    max_sales_idx = monthly['Sales'].idxmax()
    peak_month = monthly.loc[max_sales_idx, 'Year_Month']
    peak_val = monthly.loc[max_sales_idx, 'Sales']
    ax1.annotate(f'Peak: ${peak_val:,.0f}\n({peak_month})',
                 xy=(max_sales_idx, peak_val), xytext=(max_sales_idx - 2.5, peak_val + 7000),
                 arrowprops=dict(facecolor='#0F172A', arrowstyle='->', lw=1.2),
                 fontsize=8, fontweight='bold', color='#0F172A',
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="#FEF3C7", edgecolor="#F59E0B", lw=0.8))

    # -------------------------------------------------------------
    # 4. CHART 2: CUSTOMER SEGMENT BREAKDOWN (Row 2, Col 2 - Donut Chart)
    # -------------------------------------------------------------
    ax2 = fig.add_subplot(gs[2, 2])
    ax2.set_facecolor('#FFFFFF')

    segment_data = df.groupby('Segment')['Sales'].sum().reset_index()
    colors_segment = ['#3B82F6', '#10B981', '#F59E0B']

    wedges, texts, autotexts = ax2.pie(
        segment_data['Sales'],
        labels=segment_data['Segment'],
        autopct='%1.1f%%',
        startangle=140,
        pctdistance=0.72,
        colors=colors_segment,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2)
    )
    for text in texts:
        text.set_color('#1E293B')
        text.set_fontsize(9.5)
        text.set_fontweight('semibold')
    for autotext in autotexts:
        autotext.set_color('#FFFFFF')
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')

    # Center label in donut hole
    ax2.text(0, 0, f"${total_sales/1e6:.2f}M\nTotal", ha='center', va='center', fontsize=11, fontweight='bold', color='#0F172A')
    ax2.set_title("2. Revenue Share by Customer Segment", fontsize=12, fontweight='bold', color='#1E293B', pad=12, loc='left')

    # -------------------------------------------------------------
    # 5. CHART 3: SUB-CATEGORY REVENUE & PROFITABILITY (Row 3, Col 0 - Horizontal Bar)
    # -------------------------------------------------------------
    ax3 = fig.add_subplot(gs[3, 0])
    ax3.set_facecolor('#FFFFFF')

    subcat = df.groupby('Sub_Category').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values('Sales', ascending=True)
    y_pos = np.arange(len(subcat))

    bars = ax3.barh(y_pos, subcat['Sales'], height=0.65, color='#4F46E5', alpha=0.85, edgecolor='#3730A3')
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(subcat.index, fontsize=8.5, color='#334155')
    ax3.set_xlabel("Total Sales ($ USD)", fontsize=9, fontweight='bold', color='#475569')
    ax3.xaxis.set_major_formatter('${x:,.0f}')
    ax3.set_title("3. Sales Performance by Sub-Category", fontsize=12, fontweight='bold', color='#1E293B', pad=12, loc='left')
    ax3.grid(axis='x', linestyle=':', alpha=0.6, color='#CBD5E1')

    # Value labels
    for bar in bars:
        w = bar.get_width()
        ax3.text(w + 3000, bar.get_y() + bar.get_height()/2, f"${w/1000:.0f}K",
                 ha='left', va='center', fontsize=7.5, color='#1E293B', fontweight='bold')

    # -------------------------------------------------------------
    # 6. CHART 4: REGIONAL SALES & PROFIT COMPARISON (Row 3, Col 1 - Grouped Bar)
    # -------------------------------------------------------------
    ax4 = fig.add_subplot(gs[3, 1])
    ax4.set_facecolor('#FFFFFF')

    reg_data = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    x = np.arange(len(reg_data))
    width = 0.35

    b1 = ax4.bar(x - width/2, reg_data['Sales'], width, label='Revenue ($)', color='#0EA5E9', edgecolor='#0284C7')
    b2 = ax4.bar(x + width/2, reg_data['Profit'], width, label='Profit ($)', color='#10B981', edgecolor='#059669')

    ax4.set_title("4. Regional Sales vs Profit Comparison", fontsize=12, fontweight='bold', color='#1E293B', pad=12, loc='left')
    ax4.set_xticks(x)
    ax4.set_xticklabels(reg_data['Region'], fontsize=9, fontweight='semibold', color='#334155')
    ax4.yaxis.set_major_formatter('${x:,.0f}')
    ax4.grid(axis='y', linestyle=':', alpha=0.6, color='#CBD5E1')
    ax4.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#E2E8F0', fontsize=8.5, loc='upper right')

    for bar in b1:
        h = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2, h + 4000, f"${h/1000:.0f}k",
                 ha='center', va='bottom', fontsize=7.5, color='#0284C7', fontweight='bold')
    for bar in b2:
        h = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2, h + 4000, f"${h/1000:.0f}k",
                 ha='center', va='bottom', fontsize=7.5, color='#059669', fontweight='bold')

    # -------------------------------------------------------------
    # 7. CHART 5: SHIPPING MODE & DELIVERY TIMELINES (Row 3, Col 2 - Combo Card)
    # -------------------------------------------------------------
    ax5 = fig.add_subplot(gs[3, 2])
    ax5.set_facecolor('#FFFFFF')

    ship_perf = df.groupby('Shipping_Mode').agg(
        Order_Count=('Order_ID', 'count'),
        Avg_Days=('Shipping_Days', 'mean')
    ).sort_values('Order_Count', ascending=False).reset_index()

    ship_colors = ['#6366F1', '#8B5CF6', '#EC4899', '#F43F5E']
    bars_ship = ax5.bar(ship_perf['Shipping_Mode'], ship_perf['Order_Count'], color=ship_colors, width=0.55, edgecolor='#4338CA')

    ax5.set_title("5. Fulfillment Volume & Speed by Ship Mode", fontsize=12, fontweight='bold', color='#1E293B', pad=12, loc='left')
    ax5.set_ylabel("Total Orders", fontsize=9, fontweight='bold', color='#475569')
    ax5.grid(axis='y', linestyle=':', alpha=0.6, color='#CBD5E1')
    ax5.set_xticks(range(len(ship_perf)))
    ax5.set_xticklabels(ship_perf['Shipping_Mode'], rotation=20, ha='right', fontsize=8.5, color='#334155')

    # Add second axis for average delivery days
    ax5_twin = ax5.twinx()
    ax5_twin.plot(ship_perf['Shipping_Mode'], ship_perf['Avg_Days'], color='#D97706', marker='D', linewidth=2, markersize=6, label='Avg Days')
    ax5_twin.set_ylabel("Avg Delivery Days", fontsize=9, fontweight='bold', color='#D97706')
    ax5_twin.set_ylim(0, 7)
    ax5_twin.grid(False)

    for i, bar in enumerate(bars_ship):
        h = bar.get_height()
        avg_d = ship_perf.loc[i, 'Avg_Days']
        ax5.text(bar.get_x() + bar.get_width()/2, h/2, f"{h:,}\nOrders",
                 ha='center', va='center', fontsize=8, color='#FFFFFF', fontweight='bold')
        ax5_twin.text(i, avg_d + 0.35, f"{avg_d:.1f} d",
                      ha='center', va='bottom', fontsize=8, color='#B45309', fontweight='bold')

    # Save high-resolution PNG & PDF
    png_path = os.path.join(output_dir, "ecommerce_dashboard.png")
    pdf_path = os.path.join(output_dir, "ecommerce_dashboard.pdf")

    plt.savefig(png_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.savefig(pdf_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()

    print(f"Static Dashboard successfully generated:\n  - Image (PNG): {png_path}\n  - Vector PDF: {pdf_path}")
    return png_path, pdf_path

if __name__ == '__main__':
    base_dir = r"C:\Users\hegazy\.gemini\antigravity\scratch\ecommerce_dashboard"
    clean_csv = os.path.join(base_dir, "ecommerce_sales_cleaned.csv")
    build_dashboard(clean_csv, base_dir)
