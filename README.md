# Executive E-Commerce & Retail Performance Dashboard

A comprehensive, production-grade business intelligence dashboard and academic submission project built with Python. This package fulfills every requirement outlined in the Data Visualization & Dashboard Assignment brief.

---

## 📁 Repository & Submission Artifacts

| Deliverable Type | File Name | Description & Submission Role |
| :--- | :--- | :--- |
| **Dashboard (PDF)** | [`ecommerce_dashboard.pdf`](ecommerce_dashboard.pdf) | Vector, print-ready executive dashboard layout at 300 DPI. |
| **Dashboard (Image)** | [`ecommerce_dashboard.png`](ecommerce_dashboard.png) | High-resolution composite image of the complete dashboard. |
| **Dashboard (Interactive)** | [`ecommerce_dashboard.html`](ecommerce_dashboard.html) | Standalone responsive HTML5/JS dashboard with real-time filters. |
| **Description Report (Word)**| [`Dashboard_Description_Report.docx`](Dashboard_Description_Report.docx) | Fully styled Microsoft Word report with data dictionary & analysis. |
| **Description Report (PDF)** | [`Dashboard_Description_Report.pdf`](Dashboard_Description_Report.pdf) | Formal multi-page PDF report with embedded visual figures. |
| **Dataset (Raw CSV)** | [`ecommerce_sales_raw.csv`](ecommerce_sales_raw.csv) | Original raw transactional dataset (2,505 records). |
| **Dataset (Cleaned CSV)** | [`ecommerce_sales_cleaned.csv`](ecommerce_sales_cleaned.csv) | Cleaned, deduplicated, and feature-engineered dataset (2,500 records).|
| **Dataset (Cleaned Excel)** | [`ecommerce_sales_cleaned.xlsx`](ecommerce_sales_cleaned.xlsx) | Excel workbook with formatted headers. |

---

## 🚀 Key Dashboard Visualizations

1. **Top KPI Scorecards**: Total Revenue ($1,593,025), Operating Profit ($202,500), Margin (12.71%), Units Sold (6,416), Average Order Value ($637.21).
2. **Monthly Trajectory (Line/Area)**: 24-month revenue and net income tracking (2024–2025) highlighting Q4 holiday demand spikes.
3. **Customer Segment Donut**: Percentage contribution of Consumer (51%), Corporate (30%), and Home Office (19%) buyer groups.
4. **Sub-Category Performance (Ranked Bar)**: Revenue contribution across 12 distinct product lines.
5. **Regional Comparison (Grouped Bar)**: Sales versus profit margins across North, South, East, and West sales territories.
6. **Logistics & Shipping Mode (Combo Chart)**: Dispatch volume and mean delivery duration (days) across 4 shipping tiers.

---

## 🛠️ Reproduction Scripts

To regenerate any component from scratch, execute the following Python scripts in order:

```bash
# 1. Synthesize the raw multi-year transactional dataset
python generate_dataset.py

# 2. Run automated cleaning, deduplication, and feature engineering
python clean_data.py

# 3. Generate high-res static dashboard (PNG & PDF)
python generate_static_dashboard.py

# 4. Generate standalone interactive HTML5 dashboard
python generate_interactive_dashboard.py

# 5. Generate submission reports (Word & PDF)
python generate_report_docx.py
python generate_report_pdf.py
```
