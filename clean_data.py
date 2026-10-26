"""
clean_data.py
Performs data cleaning, validation, and feature engineering on the raw E-Commerce dataset.
Outputs:
- ecommerce_sales_cleaned.csv
- ecommerce_sales_cleaned.xlsx
- Detailed cleaning audit log and summary metrics
"""

import os
import pandas as pd
import numpy as np

def clean_ecommerce_data(input_csv, output_dir):
    print("=" * 60)
    print("STARTING DATA CLEANING & PREPARATION PIPELINE")
    print("=" * 60)

    # 1. Load dataset
    df = pd.read_csv(input_csv)
    initial_rows = len(df)
    print(f"Loaded {initial_rows} records from: {input_csv}")

    # 2. Check & Remove Duplicates
    num_duplicates = df.duplicated().sum()
    print(f"Duplicate records identified: {num_duplicates}")
    df = df.drop_duplicates().reset_index(drop=True)
    post_dedup_rows = len(df)

    # 3. Handle Missing Values
    null_counts = df.isnull().sum()
    print("Missing values per column before handling:")
    for col, val in null_counts.items():
        if val > 0:
            print(f"  - {col}: {val} missing ({val/post_dedup_rows*100:.2f}%)")
    
    # Impute missing Postal_Code with '90001' default/fallback
    df['Postal_Code'] = df['Postal_Code'].fillna('90001').astype(str)

    # 4. Standardize Data Types
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Ship_Date'] = pd.to_datetime(df['Ship_Date'])
    df['Unit_Price'] = df['Unit_Price'].astype(float)
    df['Quantity'] = df['Quantity'].astype(int)
    df['Discount'] = df['Discount'].astype(float)
    df['Sales'] = df['Sales'].astype(float)
    df['Profit'] = df['Profit'].astype(float)

    # 5. Feature Engineering
    print("\nEngineering derived analytical features...")
    # Date parts
    df['Order_Year'] = df['Order_Date'].dt.year
    df['Order_Month'] = df['Order_Date'].dt.strftime('%b')
    df['Order_Month_Num'] = df['Order_Date'].dt.month
    df['Year_Month'] = df['Order_Date'].dt.strftime('%Y-%m')
    df['Quarter'] = df['Order_Date'].dt.to_period('Q').astype(str)

    # Shipping Duration
    df['Shipping_Days'] = (df['Ship_Date'] - df['Order_Date']).dt.days

    # Financial Metrics
    df['Profit_Margin_Pct'] = np.where(df['Sales'] > 0, (df['Profit'] / df['Sales']) * 100, 0.0)
    df['Profit_Margin_Pct'] = df['Profit_Margin_Pct'].round(2)
    df['Profitability_Status'] = np.where(df['Profit'] >= 0, 'Profitable', 'Loss-Making')

    # Discount bracket
    def categorize_discount(disc):
        if disc == 0:
            return 'None (0%)'
        elif disc <= 0.10:
            return 'Low (1-10%)'
        elif disc <= 0.20:
            return 'Moderate (11-20%)'
        else:
            return 'High (>20%)'

    df['Discount_Bracket'] = df['Discount'].apply(categorize_discount)

    # 6. Sanity Checks & Validations
    assert (df['Shipping_Days'] >= 0).all(), "Error: Negative shipping days found!"
    assert (df['Sales'] >= 0).all(), "Error: Negative sales found!"

    # 7. Export Cleaned Dataset
    clean_csv_path = os.path.join(output_dir, "ecommerce_sales_cleaned.csv")
    clean_xlsx_path = os.path.join(output_dir, "ecommerce_sales_cleaned.xlsx")

    # Format dates back to clean ISO string for CSV
    df_export = df.copy()
    df_export['Order_Date'] = df_export['Order_Date'].dt.strftime('%Y-%m-%d')
    df_export['Ship_Date'] = df_export['Ship_Date'].dt.strftime('%Y-%m-%d')

    df_export.to_csv(clean_csv_path, index=False)
    print(f"Cleaned CSV saved to: {clean_csv_path}")

    # Export to Excel with auto-width columns
    with pd.ExcelWriter(clean_xlsx_path, engine='openpyxl') as writer:
        df_export.to_excel(writer, sheet_name='Cleaned_Sales_Data', index=False)
    print(f"Cleaned Excel saved to: {clean_xlsx_path}")

    # 8. Summary KPIs
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    overall_margin = (total_profit / total_sales) * 100
    total_units = df['Quantity'].sum()
    total_orders = df['Order_ID'].nunique()
    avg_order_value = total_sales / total_orders

    print("\n" + "=" * 60)
    print("DATA PREPARATION SUMMARY & KEY METRICS")
    print("=" * 60)
    print(f"Initial Rows:               {initial_rows:,}")
    print(f"Duplicates Removed:         {num_duplicates:,}")
    print(f"Final Clean Records:        {len(df):,}")
    print(f"Total Unique Orders:        {total_orders:,}")
    print(f"Total Revenue (Sales):      ${total_sales:,.2f}")
    print(f"Total Operating Profit:     ${total_profit:,.2f}")
    print(f"Overall Profit Margin:      {overall_margin:.2f}%")
    print(f"Total Units Sold:           {total_units:,}")
    print(f"Average Order Value (AOV):  ${avg_order_value:,.2f}")
    print("=" * 60)

    return df

if __name__ == '__main__':
    base_dir = r"C:\Users\hegazy\.gemini\antigravity\scratch\ecommerce_dashboard"
    raw_csv = os.path.join(base_dir, "ecommerce_sales_raw.csv")
    clean_ecommerce_data(raw_csv, base_dir)
