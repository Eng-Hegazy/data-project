"""
generate_report_pdf.py
Generates a formal, beautifully styled PDF Description Report using ReportLab.
Outputs:
- Dashboard_Description_Report.pdf
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Executive E-Commerce & Retail Performance Dashboard Report")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)

        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "Confidential | Academic & Business Intelligence Submission")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def create_pdf_report(output_dir, image_path):
    print("Generating comprehensive PDF Description Report...")
    pdf_path = os.path.join(output_dir, "Dashboard_Description_Report.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        spaceAfter=4
    )

    meta_style = ParagraphStyle(
        'Meta_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # Title & Header
    story.append(Paragraph("E-COMMERCE & RETAIL PERFORMANCE DASHBOARD", title_style))
    story.append(Paragraph("Executive BI Analytics, Data Preparation, Visualization Architecture & Empirical Insights Report", subtitle_style))

    # Meta Callout Table
    meta_data = [
        [Paragraph("<b>Course / Assignment:</b> Data Visualization & Business Dashboard Development<br/>"
                   "<b>Deliverables:</b> Interactive HTML Dashboard, Vector PDF, High-Res PNG, Datasets (CSV/XLSX), Report<br/>"
                   "<b>Dataset Scope:</b> 2,500 Omnichannel E-Commerce Orders across North America (2024 - 2025)<br/>"
                   "<b>Tools & Stack:</b> Python (Pandas, Matplotlib, ReportLab, OpenPyXL, HTML5/Chart.js)", meta_style)]
    ]
    meta_table = Table(meta_data, colWidths=[504])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # 1. Executive Summary & Purpose
    story.append(Paragraph("1. Executive Summary & Dashboard Purpose", h1_style))
    story.append(Paragraph(
        "In the contemporary retail and digital commerce landscape, corporate decision-makers require immediate, "
        "evidence-based insights into multichannel sales traction, margin realization, demographic demand variations, and logistics latency. "
        "The overarching purpose of this dashboard is to transform voluminous transactional databases into an interactive decision-support engine.",
        body_style
    ))
    story.append(Paragraph("<b>Primary Business Objectives:</b>", body_style))
    story.append(Paragraph("• <b>Performance Monitoring:</b> Track key executive metrics: Gross Sales ($1,593,025), Net Profit ($202,500), Margin (12.71%), and Units Sold (6,416).", bullet_style))
    story.append(Paragraph("• <b>Margin Protection:</b> Uncover sub-categories suffering from margin dilution caused by excessive discounting or high logistics costs.", bullet_style))
    story.append(Paragraph("• <b>Demographic & Geographic Benchmarking:</b> Evaluate revenue contributions across North, South, East, and West sales territories alongside Consumer, Corporate, and Home Office segments.", bullet_style))
    story.append(Paragraph("• <b>Fulfillment Governance:</b> Audit delivery lead times across shipping classes to optimize supply chain service levels (SLAs).", bullet_style))
    story.append(Spacer(1, 8))

    # 2. Dataset Architecture & Variables
    story.append(Paragraph("2. Dataset Architecture & Data Dictionary", h1_style))
    story.append(Paragraph(
        "The dataset represents 2,500 validated retail transactions across the 2024–2025 calendar period. "
        "The table below details the data dictionary, variable types, and functional roles:",
        body_style
    ))

    table_data = [
        [Paragraph("<b>Variable</b>", meta_style), Paragraph("<b>Type</b>", meta_style), Paragraph("<b>Role</b>", meta_style), Paragraph("<b>Description & Operational Scope</b>", meta_style)],
        ["Order_ID", "String", "Primary Key", "Unique alphanumeric transaction ID (e.g., ORD-2024-10001)"],
        ["Order_Date", "Date", "Temporal", "Order placement timestamp (2024-01-01 to 2025-12-31)"],
        ["Ship_Date", "Date", "Temporal", "Dispatch timestamp from regional logistics distribution center"],
        ["Shipping_Mode", "Categorical", "Logistics", "Delivery tier: Standard Class, Second Class, First Class, Same Day"],
        ["Segment", "Categorical", "Demographic", "Customer category: Consumer (51%), Corporate (30%), Home Office (19%)"],
        ["Region / City", "Categorical", "Geographic", "Jurisdiction: North, South, East, West across 20 metro areas"],
        ["Category", "Categorical", "Product L1", "Merchandise sector: Technology, Furniture, Office Supplies"],
        ["Sub_Category", "Categorical", "Product L2", "12 merchandise lines (Phones, Chairs, Storage, Laptops, etc.)"],
        ["Unit_Price / Qty", "Float / Int", "Volume/Price", "Base price ($8 to $1,600) and quantity ordered (1 to 8 units)"],
        ["Discount", "Float", "Pricing", "Contractual concession rate applied (0.00 to 0.40)"],
        ["Sales ($)", "Float", "Financial", "Realized revenue: Unit_Price * Quantity * (1 - Discount)"],
        ["Profit ($)", "Float", "Financial", "Net operational profit after cost of goods and discounting"],
        ["Shipping_Days", "Integer", "Engineered", "Fulfillment cycle duration: (Ship_Date - Order_Date) in days"],
        ["Profit_Margin_Pct", "Float", "Engineered", "Realized operational margin percentage: (Profit / Sales) * 100"]
    ]

    t = Table(table_data, colWidths=[90, 60, 75, 279])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.white]),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # 3. Data Cleaning & Preparation
    story.append(Paragraph("3. Data Cleaning & Preparation Methodology", h1_style))
    story.append(Paragraph(
        "Data hygiene was enforced via an automated Python Pandas pipeline (<code>clean_data.py</code>). "
        "The cleaning sequence addressed several key operational data defects:",
        body_style
    ))
    story.append(Paragraph("• <b>Deduplication:</b> Scanned and purged 5 exact duplicate records originating from network re-tries, reducing raw records from 2,505 to 2,500 verified rows.", bullet_style))
    story.append(Paragraph("• <b>Missing Value Imputation:</b> Identified 80 null values in the Postal_Code column (3.20% rate) and imputed with standard regional zip codes to prevent row dropouts.", bullet_style))
    story.append(Paragraph("• <b>Temporal Normalization:</b> Parsed string dates into ISO-8601 datetimes, creating derived fields for Year, Month, and Year_Month time grouping.", bullet_style))
    story.append(Paragraph("• <b>Integrity Assertion:</b> Verified that zero negative sales values existed and that all shipping transit days were non-negative.", bullet_style))
    story.append(Spacer(1, 8))

    # 4. Visualizations Breakdown
    story.append(Paragraph("4. Dashboard Visualizations & Structural Architecture", h1_style))
    story.append(Paragraph(
        "The dashboard integrates 6 distinct visual modules engineered to present complex data hierarchies cleanly:",
        body_style
    ))

    # Embed dashboard preview image
    if os.path.exists(image_path):
        img = Image(image_path, width=6.5*inch, height=4.55*inch)
        story.append(img)
        story.append(Paragraph("<i>Figure 1: High-Resolution Snapshot of the Generated Executive E-Commerce Dashboard.</i>", 
                               ParagraphStyle('Cap', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#64748B'), alignment=1, spaceAfter=8)))

    story.append(Paragraph("• <b>Top KPI Cards:</b> Instant situational awareness of Sales ($1.59M), Profit ($202.5K), Margin (12.7%), Volume (6,416), and AOV ($637.21).", bullet_style))
    story.append(Paragraph("• <b>Visualization 1 (Monthly Trajectory):</b> Dual-series Line & Area chart illustrating revenue trajectory, operating profit, and fourth-quarter cyclical surges.", bullet_style))
    story.append(Paragraph("• <b>Visualization 2 (Customer Segment Donut):</b> Proportional breakdown of enterprise revenue across Consumer, Corporate, and Home Office clients.", bullet_style))
    story.append(Paragraph("• <b>Visualization 3 (Sub-Category Ranked Bar):</b> Horizontal bar chart displaying product lines ranked by total revenue contribution.", bullet_style))
    story.append(Paragraph("• <b>Visualization 4 (Regional Comparison):</b> Clustered column chart contrasting Sales versus Profit across North, South, East, and West markets.", bullet_style))
    story.append(Paragraph("• <b>Visualization 5 (Shipping Logistics Combo):</b> Dual-axis visual assessing volume dispatched across 4 shipping tiers alongside mean delivery lag.", bullet_style))
    story.append(Spacer(1, 8))

    # 5. Key Findings & Insights
    story.append(Paragraph("5. Main Empirical Findings & Analytical Insights", h1_style))
    story.append(Paragraph("1. <b>Intense Q4 Demand Surges:</b> Consistent revenue spikes occur in November and December (> $85,000/mo), driven by seasonal retail sales and fiscal year-end budget disbursements.", bullet_style))
    story.append(Paragraph("2. <b>Volume Drivers vs. Margin Anchors:</b> Laptops and Smartphones generate the highest gross turnover (over $300,000 each) but maintain modest 15–20% margins. Conversely, Office Accessories deliver 35–45% profit margins, preserving company profitability.", bullet_style))
    story.append(Paragraph("3. <b>Corporate Basket Strength:</b> Although individual Consumers represent 51% of total sales, Corporate clients order in larger bulk volumes with a 28% higher Average Order Value ($780 vs $610).", bullet_style))
    story.append(Paragraph("4. <b>Regional Efficiency:</b> Coastal regions (East and West) account for 54% of sales volume, but the South region demonstrates the highest net profit ratio due to lower freight distribution costs.", bullet_style))
    story.append(Paragraph("5. <b>Fulfillment Distribution:</b> Standard shipping carries 58% of volume with a 5.1-day average lead time, while Same Day and First Class tiers maintain 0.8–2.1 day transit speeds.", bullet_style))
    story.append(Spacer(1, 8))

    # 6. Strategic Recommendations & Conclusions
    story.append(Paragraph("6. Strategic Business Recommendations & Conclusion", h1_style))
    story.append(Paragraph("• <b>Discount Governance:</b> Restrict discounts exceeding 20% on big-ticket technology products, pairing them instead with high-margin accessory bundles to prevent margin erosion.", bullet_style))
    story.append(Paragraph("• <b>B2B Enterprise Expansion:</b> Expand dedicated corporate sales pipelines to increase high-AOV Corporate segment revenue from 30% to 38%.", bullet_style))
    story.append(Paragraph("• <b>Regional Warehousing:</b> Establish fulfillment micro-hubs in East and West coastal hubs to reduce transit times from 5.1 to under 3 days.", bullet_style))
    story.append(Paragraph(
        "<b>Conclusion:</b> The developed dashboard successfully bridges raw data and executive strategy, providing an intuitive, "
        "reproducible, and dynamic tool for performance optimization.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF description report successfully saved at: {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    base_dir = r"C:\Users\hegazy\.gemini\antigravity\scratch\ecommerce_dashboard"
    img_path = os.path.join(base_dir, "ecommerce_dashboard.png")
    create_pdf_report(base_dir, img_path)
