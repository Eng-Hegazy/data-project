"""
generate_dataset.py
Generates a realistic, comprehensive Global E-Commerce & Retail Sales Dataset (2024 - 2025).
Contains order details, customer segments, regional markets, product categories,
pricing, discounts, profit margins, and shipping logistics.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def create_ecommerce_dataset(num_records=2500, random_seed=42):
    random.seed(random_seed)
    np.random.seed(random_seed)

    # Categories and sub-categories with realistic pricing and base profit margins
    catalog = {
        'Technology': {
            'Phones & Smartphones': {'base_price': (150, 950), 'margin_range': (0.15, 0.32)},
            'Laptops & Computers': {'base_price': (400, 1600), 'margin_range': (0.12, 0.28)},
            'Accessories & Cables': {'base_price': (15, 90), 'margin_range': (0.28, 0.55)},
            'Printers & Scanners': {'base_price': (120, 550), 'margin_range': (0.05, 0.22)},
        },
        'Furniture': {
            'Office Chairs': {'base_price': (80, 420), 'margin_range': (0.10, 0.26)},
            'Desks & Workstations': {'base_price': (180, 750), 'margin_range': (0.08, 0.24)},
            'Bookcases & Shelves': {'base_price': (90, 360), 'margin_range': (-0.05, 0.18)},
            'Furnishings & Decor': {'base_price': (25, 140), 'margin_range': (0.15, 0.35)},
        },
        'Office Supplies': {
            'Paper Products': {'base_price': (10, 55), 'margin_range': (0.20, 0.45)},
            'Storage & Organization': {'base_price': (20, 110), 'margin_range': (0.18, 0.38)},
            'Binders & Fasteners': {'base_price': (8, 40), 'margin_range': (0.25, 0.50)},
            'Art & Writing Supplies': {'base_price': (12, 75), 'margin_range': (0.22, 0.42)},
        }
    }

    segments = ['Consumer', 'Corporate', 'Home Office']
    segment_weights = [0.52, 0.30, 0.18]

    regions = {
        'North': ['Chicago', 'Detroit', 'Minneapolis', 'Milwaukee', 'Cleveland'],
        'South': ['Houston', 'Atlanta', 'Miami', 'Dallas', 'Charlotte'],
        'East': ['New York City', 'Philadelphia', 'Boston', 'Pittsburgh', 'Baltimore'],
        'West': ['Los Angeles', 'San Francisco', 'Seattle', 'Denver', 'Phoenix']
    }
    region_weights = [0.24, 0.22, 0.28, 0.26]

    shipping_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
    shipping_weights = [0.58, 0.20, 0.16, 0.06]

    customer_pool = [f"CUST-{1000 + i}" for i in range(400)]
    customer_names = [
        "James Wilson", "Mary Johnson", "Robert Smith", "Patricia Brown", "Michael Davis",
        "Jennifer Miller", "William Wilson", "Elizabeth Moore", "David Taylor", "Barbara Anderson",
        "Richard Thomas", "Susan Jackson", "Joseph White", "Jessica Harris", "Thomas Martin",
        "Sarah Thompson", "Charles Garcia", "Karen Martinez", "Christopher Robinson", "Nancy Clark",
        "Daniel Rodriguez", "Lisa Lewis", "Matthew Lee", "Betty Walker", "Anthony Hall",
        "Margaret Allen", "Mark Young", "Sandra Hernandez", "Donald King", "Ashley Wright"
    ]

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    date_range_days = (end_date - start_date).days

    records = []

    for i in range(1, num_records + 1):
        order_id = f"ORD-{2024 + (i % 2)}-{10000 + i}"
        
        # Seasonality: higher chance in Q4 (Nov, Dec) and back-to-school (Aug, Sep)
        day_offset = random.randint(0, date_range_days)
        order_date = start_date + timedelta(days=day_offset)
        
        # Boost Q4 frequency
        if order_date.month in [11, 12] and random.random() < 0.25:
            day_offset = random.randint(0, date_range_days)
            order_date = start_date + timedelta(days=day_offset)

        cust_idx = random.randint(0, len(customer_pool) - 1)
        customer_id = customer_pool[cust_idx]
        customer_name = customer_names[cust_idx % len(customer_names)]
        segment = random.choices(segments, weights=segment_weights)[0]

        region = random.choices(list(regions.keys()), weights=region_weights)[0]
        city = random.choice(regions[region])

        category = random.choices(list(catalog.keys()), weights=[0.38, 0.30, 0.32])[0]
        sub_category = random.choice(list(catalog[category].keys()))
        prod_meta = catalog[category][sub_category]

        unit_price = round(random.uniform(prod_meta['base_price'][0], prod_meta['base_price'][1]), 2)
        quantity = random.choices([1, 2, 3, 4, 5, 6, 7, 8], weights=[0.35, 0.25, 0.15, 0.10, 0.06, 0.04, 0.03, 0.02])[0]
        
        # Discounts: 0%, 10%, 15%, 20%, occasionally 30% or 40%
        discount = random.choices([0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40], weights=[0.45, 0.15, 0.15, 0.10, 0.08, 0.05, 0.02])[0]
        
        gross_sales = round(unit_price * quantity, 2)
        sales = round(gross_sales * (1.0 - discount), 2)

        # Profit calculation with impact of high discounts
        base_margin = random.uniform(prod_meta['margin_range'][0], prod_meta['margin_range'][1])
        # High discounts erode margin sharply
        effective_margin = base_margin - (discount * 0.95)
        profit = round(sales * effective_margin, 2)

        shipping_mode = random.choices(shipping_modes, weights=shipping_weights)[0]
        
        # Ship date calculation based on mode
        ship_delay_map = {
            'Same Day': (0, 1),
            'First Class': (1, 3),
            'Second Class': (2, 5),
            'Standard Class': (3, 7)
        }
        delay = random.randint(ship_delay_map[shipping_mode][0], ship_delay_map[shipping_mode][1])
        ship_date = order_date + timedelta(days=delay)

        # Introduce a few realistic raw data anomalies (e.g. minor missing postal code, notes)
        postal_code = f"{random.randint(10000, 99950)}" if random.random() > 0.03 else None
        order_priority = random.choices(['Low', 'Medium', 'High', 'Critical'], weights=[0.20, 0.45, 0.25, 0.10])[0]

        records.append({
            'Order_ID': order_id,
            'Order_Date': order_date.strftime('%Y-%m-%d'),
            'Ship_Date': ship_date.strftime('%Y-%m-%d'),
            'Shipping_Mode': shipping_mode,
            'Customer_ID': customer_id,
            'Customer_Name': customer_name,
            'Segment': segment,
            'City': city,
            'Region': region,
            'Postal_Code': postal_code,
            'Category': category,
            'Sub_Category': sub_category,
            'Unit_Price': unit_price,
            'Quantity': quantity,
            'Discount': discount,
            'Sales': sales,
            'Profit': profit,
            'Order_Priority': order_priority
        })

    df = pd.DataFrame(records)
    
    # Intentionally add 5 duplicate rows to represent raw data collection duplicates
    duplicates = df.iloc[:5].copy()
    df_raw = pd.concat([df, duplicates], ignore_index=True)
    
    return df_raw

if __name__ == '__main__':
    base_dir = r"C:\Users\hegazy\.gemini\antigravity\scratch\ecommerce_dashboard"
    os.makedirs(base_dir, exist_ok=True)
    raw_df = create_ecommerce_dataset(num_records=2500)
    raw_csv_path = os.path.join(base_dir, "ecommerce_sales_raw.csv")
    raw_df.to_csv(raw_csv_path, index=False)
    print(f"Generated raw dataset: {raw_csv_path} with {len(raw_df)} records.")
