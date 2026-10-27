"""
generate_interactive_dashboard.py
Generates a 100% self-contained, robust HTML5/CSS3 interactive dashboard.
Features:
- Pure embedded CSS (NO runtime Tailwind JS required - renders identically everywhere, even in sandboxed iframes)
- Explicit SVG dimensions (prevents any icon blowout or rendering bugs)
- Chart.js visualizations with responsive charts, tooltips, and interactive filter controls
- Dynamic live KPI recalculation across Region, Category, and Fiscal Year
- Responsive layout for desktop and mobile
"""

import os
import json
import pandas as pd

def build_interactive_dashboard(clean_csv_path, output_dir):
    print("Generating bulletproof interactive HTML dashboard...")
    df = pd.read_csv(clean_csv_path)

    records = df[[
        'Order_ID', 'Order_Date', 'Order_Year', 'Year_Month',
        'Region', 'Category', 'Sub_Category', 'Segment',
        'Sales', 'Profit', 'Quantity', 'Shipping_Mode', 'Shipping_Days', 'Discount'
    ]].to_dict(orient='records')

    data_json = json.dumps(records)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Executive Sales & Profitability Dashboard</title>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-page: #f8fafc;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --card-bg: #ffffff;
            --border-color: #e2e8f0;
            --blue: #2563eb;
            --emerald: #059669;
            --teal: #0d9488;
            --amber: #d97706;
            --purple: #7c3aed;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            padding: 20px;
            line-height: 1.5;
        }}

        .container {{
            max-width: 1280px;
            margin: 0 auto;
        }}

        /* Header */
        .header {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border-radius: 16px;
            padding: 24px 28px;
            color: #ffffff;
            margin-bottom: 20px;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}

        .badge {{
            display: inline-block;
            background-color: #3b82f6;
            color: #ffffff;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 999px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .sub-badge {{
            font-size: 12px;
            color: #94a3b8;
            margin-left: 8px;
        }}

        .header h1 {{
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-bottom: 4px;
        }}

        .header p {{
            font-size: 13px;
            color: #94a3b8;
        }}

        .header-actions {{
            display: flex;
            gap: 10px;
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            font-weight: 600;
            padding: 9px 16px;
            border-radius: 8px;
            cursor: pointer;
            border: 1px solid transparent;
            transition: all 0.2s ease;
            text-decoration: none;
        }}

        .btn svg {{
            width: 15px;
            height: 15px;
            flex-shrink: 0;
        }}

        .btn-outline {{
            background-color: #1e293b;
            color: #e2e8f0;
            border-color: #334155;
        }}
        .btn-outline:hover {{
            background-color: #334155;
        }}

        .btn-primary {{
            background-color: #2563eb;
            color: #ffffff;
        }}
        .btn-primary:hover {{
            background-color: #1d4ed8;
        }}

        /* Filters Bar */
        .filter-bar {{
            background-color: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 14px 20px;
            margin-bottom: 20px;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 14px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}

        .filter-label-group {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            font-weight: 700;
            color: #334155;
        }}

        .filter-label-group svg {{
            width: 16px;
            height: 16px;
            color: #2563eb;
        }}

        .filter-controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .filter-item {{
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}

        .filter-item label {{
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .filter-item select {{
            font-size: 12px;
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid #cbd5e1;
            background-color: #f8fafc;
            color: var(--text-main);
            font-weight: 500;
            cursor: pointer;
            outline: none;
        }}
        .filter-item select:focus {{
            border-color: #2563eb;
            background-color: #ffffff;
        }}

        /* KPIs Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 14px;
            margin-bottom: 20px;
        }}

        .kpi-card {{
            background-color: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            border-left: 4px solid var(--blue);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .kpi-card.green {{ border-left-color: var(--emerald); }}
        .kpi-card.teal {{ border-left-color: var(--teal); }}
        .kpi-card.amber {{ border-left-color: var(--amber); }}
        .kpi-card.purple {{ border-left-color: var(--purple); }}

        .kpi-title {{
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .kpi-value {{
            font-size: 22px;
            font-weight: 800;
            color: var(--text-main);
            margin: 6px 0 2px 0;
            letter-spacing: -0.5px;
        }}

        .kpi-sub {{
            font-size: 11px;
            font-weight: 600;
            color: var(--blue);
        }}
        .kpi-card.green .kpi-sub {{ color: var(--emerald); }}
        .kpi-card.teal .kpi-sub {{ color: var(--teal); }}
        .kpi-card.amber .kpi-sub {{ color: var(--amber); }}
        .kpi-card.purple .kpi-sub {{ color: var(--purple); }}

        /* Charts Layout */
        .chart-row-1 {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 16px;
            margin-bottom: 16px;
        }}

        .chart-row-2 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }}

        .chart-card {{
            background-color: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }}

        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 14px;
        }}

        .chart-header h2 {{
            font-size: 14px;
            font-weight: 700;
            color: var(--text-main);
        }}

        .chart-header p {{
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 2px;
        }}

        .chart-container {{
            position: relative;
            width: 100%;
            height: 280px;
        }}

        /* Table Card */
        .table-card {{
            background-color: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            text-align: left;
        }}

        thead tr {{
            background-color: #f8fafc;
            border-bottom: 1px solid var(--border-color);
        }}

        th {{
            padding: 10px 12px;
            font-size: 10px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #f1f5f9;
            color: #334155;
        }}

        tr:hover td {{
            background-color: #f8fafc;
        }}

        .text-right {{
            text-align: right;
        }}

        .margin-badge {{
            display: inline-block;
            padding: 2px 7px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 11px;
        }}
        .margin-high {{ background-color: #ecfdf5; color: #047857; }}
        .margin-med {{ background-color: #eff6ff; color: #1d4ed8; }}
        .margin-low {{ background-color: #fffbeb; color: #b45309; }}

        /* Footer */
        .footer {{
            text-align: center;
            font-size: 11px;
            color: var(--text-muted);
            padding: 16px 0;
            border-top: 1px solid var(--border-color);
        }}

        @media (max-width: 900px) {{
            .chart-row-1 {{
                grid-template-columns: 1fr;
            }}
            .header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}

        @media print {{
            .no-print {{ display: none !important; }}
            body {{ background-color: #ffffff; padding: 0; }}
            .card-shadow, .header, .chart-card, .table-card {{ box-shadow: none !important; }}
        }}
    </style>
</head>
<body>

    <div class="container">
        <!-- Top Header -->
        <header class="header">
            <div>
                <div>
                    <span class="badge">Business Intelligence</span>
                    <span class="sub-badge">2024 - 2025 Multi-Year Analytics</span>
                </div>
                <h1>Executive E-Commerce & Retail Dashboard</h1>
                <p>Holistic analysis of revenue, margin performance, customer segments, and fulfillment logistics.</p>
            </div>
            <div class="header-actions no-print">
                <button onclick="window.print()" class="btn btn-outline">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="6 9 6 2 18 2 18 9"></polyline>
                        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                        <rect x="6" y="14" width="12" height="8"></rect>
                    </svg>
                    Print / Export PDF
                </button>
                <button onclick="resetFilters()" class="btn btn-primary">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"></path>
                    </svg>
                    Reset Filters
                </button>
            </div>
        </header>

        <!-- Interactive Filters Bar -->
        <div class="filter-bar no-print">
            <div class="filter-label-group">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
                </svg>
                <span>Interactive Filters:</span>
            </div>
            <div class="filter-controls">
                <div class="filter-item">
                    <label>Region</label>
                    <select id="filterRegion" onchange="applyFilters()">
                        <option value="All">All Regions (4)</option>
                        <option value="North">North</option>
                        <option value="South">South</option>
                        <option value="East">East</option>
                        <option value="West">West</option>
                    </select>
                </div>
                <div class="filter-item">
                    <label>Product Category</label>
                    <select id="filterCategory" onchange="applyFilters()">
                        <option value="All">All Categories (3)</option>
                        <option value="Technology">Technology</option>
                        <option value="Furniture">Furniture</option>
                        <option value="Office Supplies">Office Supplies</option>
                    </select>
                </div>
                <div class="filter-item">
                    <label>Fiscal Year</label>
                    <select id="filterYear" onchange="applyFilters()">
                        <option value="All">All Years (2024 - 2025)</option>
                        <option value="2024">FY 2024</option>
                        <option value="2025">FY 2025</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- 5 KPI Cards -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <span class="kpi-title">Total Sales</span>
                <div id="kpiRevenue" class="kpi-value">$0</div>
                <span class="kpi-sub">Gross Realized Sales</span>
            </div>
            <div class="kpi-card green">
                <span class="kpi-title">Total Profit</span>
                <div id="kpiProfit" class="kpi-value">$0</div>
                <span class="kpi-sub">Net Operating Margin</span>
            </div>
            <div class="kpi-card teal">
                <span class="kpi-title">Profit Margin</span>
                <div id="kpiMargin" class="kpi-value">0.0%</div>
                <span class="kpi-sub">Target Benchmark: >12.0%</span>
            </div>
            <div class="kpi-card amber">
                <span class="kpi-title">Units Sold</span>
                <div id="kpiUnits" class="kpi-value">0</div>
                <span class="kpi-sub">Completed Dispatches</span>
            </div>
            <div class="kpi-card purple">
                <span class="kpi-title">Avg Order Value</span>
                <div id="kpiAOV" class="kpi-value">$0.00</div>
                <span class="kpi-sub">Revenue Per Basket</span>
            </div>
        </div>

        <!-- Chart Row 1: Monthly Trend + Segment Donut -->
        <div class="chart-row-1">
            <div class="chart-card">
                <div class="chart-header">
                    <div>
                        <h2>1. Monthly Revenue & Operating Profit Trajectory</h2>
                        <p>Longitudinal analysis showing revenue trajectory and seasonal spikes</p>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="chartTrend"></canvas>
                </div>
            </div>

            <div class="chart-card">
                <div class="chart-header">
                    <div>
                        <h2>2. Customer Segment Distribution</h2>
                        <p>Revenue split across demographic client segments</p>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="chartSegment"></canvas>
                </div>
            </div>
        </div>

        <!-- Chart Row 2: Sub-category + Region + Shipping -->
        <div class="chart-row-2">
            <div class="chart-card">
                <div class="chart-header">
                    <div>
                        <h2>3. Sales by Product Sub-Category</h2>
                        <p>Comparative revenue contribution by product line</p>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="chartSubcat"></canvas>
                </div>
            </div>

            <div class="chart-card">
                <div class="chart-header">
                    <div>
                        <h2>4. Regional Sales vs. Profit Comparison</h2>
                        <p>Geographic performance and margin realization</p>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="chartRegion"></canvas>
                </div>
            </div>

            <div class="chart-card">
                <div class="chart-header">
                    <div>
                        <h2>5. Logistics & Shipping Mode Performance</h2>
                        <p>Order volume by fulfillment shipping class</p>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="chartShip"></canvas>
                </div>
            </div>
        </div>

        <!-- Table Card -->
        <div class="table-card">
            <div class="chart-header">
                <div>
                    <h2>6. Sub-Category Performance Summary Matrix</h2>
                    <p>Aggregated sales, profit, margin %, and fulfillment efficiency</p>
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Sub-Category</th>
                        <th>Category</th>
                        <th class="text-right">Orders</th>
                        <th class="text-right">Units Sold</th>
                        <th class="text-right">Total Revenue</th>
                        <th class="text-right">Operating Profit</th>
                        <th class="text-right">Profit Margin %</th>
                    </tr>
                </thead>
                <tbody id="tableBody"></tbody>
            </table>
        </div>

        <!-- Footer -->
        <footer class="footer">
            E-Commerce Executive Analytics Dashboard | Prepared with Python, HTML5, Chart.js & Vanilla CSS | Academic Project Submission
        </footer>
    </div>

    <!-- Reactive Logic -->
    <script>
        const rawData = {data_json};

        let chartTrendInstance = null;
        let chartSegmentInstance = null;
        let chartSubcatInstance = null;
        let chartRegionInstance = null;
        let chartShipInstance = null;

        function formatCurrency(val) {{
            return '$' + Math.round(val).toLocaleString();
        }}

        function getFilteredData() {{
            const reg = document.getElementById('filterRegion').value;
            const cat = document.getElementById('filterCategory').value;
            const yr = document.getElementById('filterYear').value;

            return rawData.filter(d => {{
                if (reg !== 'All' && d.Region !== reg) return false;
                if (cat !== 'All' && d.Category !== cat) return false;
                if (yr !== 'All' && String(d.Order_Year) !== yr) return false;
                return true;
            }});
        }}

        function updateKPIs(data) {{
            const totalSales = data.reduce((sum, d) => sum + d.Sales, 0);
            const totalProfit = data.reduce((sum, d) => sum + d.Profit, 0);
            const totalUnits = data.reduce((sum, d) => sum + d.Quantity, 0);
            const orderCount = new Set(data.map(d => d.Order_ID)).size;
            const profitMargin = totalSales > 0 ? (totalProfit / totalSales) * 100 : 0;
            const aov = orderCount > 0 ? totalSales / orderCount : 0;

            document.getElementById('kpiRevenue').textContent = formatCurrency(totalSales);
            document.getElementById('kpiProfit').textContent = formatCurrency(totalProfit);
            document.getElementById('kpiMargin').textContent = profitMargin.toFixed(1) + '%';
            document.getElementById('kpiUnits').textContent = totalUnits.toLocaleString();
            document.getElementById('kpiAOV').textContent = '$' + aov.toFixed(2);
        }}

        function renderTrendChart(data) {{
            const monthMap = {{}};
            data.forEach(d => {{
                if (!monthMap[d.Year_Month]) {{
                    monthMap[d.Year_Month] = {{ sales: 0, profit: 0 }};
                }}
                monthMap[d.Year_Month].sales += d.Sales;
                monthMap[d.Year_Month].profit += d.Profit;
            }});

            const sortedMonths = Object.keys(monthMap).sort();
            const salesData = sortedMonths.map(m => Math.round(monthMap[m].sales));
            const profitData = sortedMonths.map(m => Math.round(monthMap[m].profit));

            if (chartTrendInstance) chartTrendInstance.destroy();

            const ctx = document.getElementById('chartTrend').getContext('2d');
            chartTrendInstance = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: sortedMonths,
                    datasets: [
                        {{
                            label: 'Revenue ($)',
                            data: salesData,
                            borderColor: '#2563EB',
                            backgroundColor: 'rgba(37, 99, 235, 0.12)',
                            fill: true,
                            tension: 0.3,
                            borderWidth: 2.5
                        }},
                        {{
                            label: 'Operating Profit ($)',
                            data: profitData,
                            borderColor: '#059669',
                            backgroundColor: 'rgba(5, 150, 105, 0.05)',
                            borderDash: [5, 5],
                            tension: 0.3,
                            borderWidth: 2
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {{ mode: 'index', intersect: false }},
                    plugins: {{
                        legend: {{ position: 'top', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }}
                    }},
                    scales: {{
                        y: {{
                            ticks: {{ callback: value => '$' + (value/1000) + 'k' }},
                            grid: {{ color: '#f1f5f9' }}
                        }},
                        x: {{ grid: {{ display: false }} }}
                    }}
                }}
            }});
        }}

        function renderSegmentChart(data) {{
            const segMap = {{ 'Consumer': 0, 'Corporate': 0, 'Home Office': 0 }};
            data.forEach(d => {{
                if (segMap[d.Segment] !== undefined) {{
                    segMap[d.Segment] += d.Sales;
                }}
            }});

            if (chartSegmentInstance) chartSegmentInstance.destroy();

            const ctx = document.getElementById('chartSegment').getContext('2d');
            chartSegmentInstance = new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: Object.keys(segMap),
                    datasets: [{{
                        data: Object.values(segMap).map(v => Math.round(v)),
                        backgroundColor: ['#2563EB', '#059669', '#D97706'],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }}
                    }},
                    cutout: '65%'
                }}
            }});
        }}

        function renderSubcatChart(data) {{
            const subMap = {{}};
            data.forEach(d => {{
                subMap[d.Sub_Category] = (subMap[d.Sub_Category] || 0) + d.Sales;
            }});

            const sorted = Object.entries(subMap).sort((a, b) => b[1] - a[1]);
            const labels = sorted.map(s => s[0]);
            const values = sorted.map(s => Math.round(s[1]));

            if (chartSubcatInstance) chartSubcatInstance.destroy();

            const ctx = document.getElementById('chartSubcat').getContext('2d');
            chartSubcatInstance = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: 'Sales ($)',
                        data: values,
                        backgroundColor: '#4f46e5',
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        x: {{
                            ticks: {{ callback: value => '$' + (value/1000) + 'k' }},
                            grid: {{ color: '#f1f5f9' }}
                        }},
                        y: {{ grid: {{ display: false }} }}
                    }}
                }}
            }});
        }}

        function renderRegionChart(data) {{
            const regMap = {{}};
            data.forEach(d => {{
                if (!regMap[d.Region]) {{
                    regMap[d.Region] = {{ sales: 0, profit: 0 }};
                }}
                regMap[d.Region].sales += d.Sales;
                regMap[d.Region].profit += d.Profit;
            }});

            const regions = Object.keys(regMap).sort();
            const sales = regions.map(r => Math.round(regMap[r].sales));
            const profits = regions.map(r => Math.round(regMap[r].profit));

            if (chartRegionInstance) chartRegionInstance.destroy();

            const ctx = document.getElementById('chartRegion').getContext('2d');
            chartRegionInstance = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: regions,
                    datasets: [
                        {{ label: 'Revenue ($)', data: sales, backgroundColor: '#0284c7', borderRadius: 4 }},
                        {{ label: 'Profit ($)', data: profits, backgroundColor: '#059669', borderRadius: 4 }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'top', labels: {{ boxWidth: 12, font: {{ size: 10 }} }} }}
                    }},
                    scales: {{
                        y: {{
                            ticks: {{ callback: value => '$' + (value/1000) + 'k' }},
                            grid: {{ color: '#f1f5f9' }}
                        }},
                        x: {{ grid: {{ display: false }} }}
                    }}
                }}
            }});
        }}

        function renderShipChart(data) {{
            const shipMap = {{}};
            data.forEach(d => {{
                if (!shipMap[d.Shipping_Mode]) {{
                    shipMap[d.Shipping_Mode] = 0;
                }}
                shipMap[d.Shipping_Mode] += 1;
            }});

            const modes = Object.keys(shipMap);
            const counts = modes.map(m => shipMap[m]);

            if (chartShipInstance) chartShipInstance.destroy();

            const ctx = document.getElementById('chartShip').getContext('2d');
            chartShipInstance = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: modes,
                    datasets: [{{
                        label: 'Orders Dispatched',
                        data: counts,
                        backgroundColor: ['#6366f1', '#8b5cf6', '#ec4899', '#f43f5e'],
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        y: {{ grid: {{ color: '#f1f5f9' }} }},
                        x: {{ grid: {{ display: false }} }}
                    }}
                }}
            }});
        }}

        function renderTable(data) {{
            const subMap = {{}};
            data.forEach(d => {{
                if (!subMap[d.Sub_Category]) {{
                    subMap[d.Sub_Category] = {{
                        category: d.Category,
                        orders: 0,
                        units: 0,
                        sales: 0,
                        profit: 0
                    }};
                }}
                subMap[d.Sub_Category].orders += 1;
                subMap[d.Sub_Category].units += d.Quantity;
                subMap[d.Sub_Category].sales += d.Sales;
                subMap[d.Sub_Category].profit += d.Profit;
            }});

            const sorted = Object.entries(subMap).sort((a, b) => b[1].sales - a[1].sales);
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';

            sorted.forEach(([name, val]) => {{
                const margin = val.sales > 0 ? (val.profit / val.sales) * 100 : 0;
                const marginClass = margin >= 15 ? 'margin-high' : (margin >= 8 ? 'margin-med' : 'margin-low');

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td style="font-weight: 600;">${{name}}</td>
                    <td style="color: #64748b;">${{val.category}}</td>
                    <td class="text-right">${{val.orders.toLocaleString()}}</td>
                    <td class="text-right">${{val.units.toLocaleString()}}</td>
                    <td class="text-right" style="font-weight: 600;">${{formatCurrency(val.sales)}}</td>
                    <td class="text-right" style="font-weight: 600; color: #059669;">${{formatCurrency(val.profit)}}</td>
                    <td class="text-right">
                        <span class="margin-badge ${{marginClass}}">
                            ${{margin.toFixed(1)}}%
                        </span>
                    </td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function applyFilters() {{
            const filtered = getFilteredData();
            updateKPIs(filtered);
            renderTrendChart(filtered);
            renderSegmentChart(filtered);
            renderSubcatChart(filtered);
            renderRegionChart(filtered);
            renderShipChart(filtered);
            renderTable(filtered);
        }}

        function resetFilters() {{
            document.getElementById('filterRegion').value = 'All';
            document.getElementById('filterCategory').value = 'All';
            document.getElementById('filterYear').value = 'All';
            applyFilters();
        }}

        window.addEventListener('DOMContentLoaded', () => {{
            applyFilters();
        }});
    </script>
</body>
</html>
"""

    html_path = os.path.join(output_dir, "ecommerce_dashboard.html")
    index_path = os.path.join(output_dir, "index.html")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated clean pure-CSS interactive dashboards:\n  - {html_path}\n  - {index_path}")
    return html_path

if __name__ == '__main__':
    base_dir = r"C:\Users\hegazy\.gemini\antigravity\scratch\ecommerce_dashboard"
    clean_csv = os.path.join(base_dir, "ecommerce_sales_cleaned.csv")
    build_interactive_dashboard(clean_csv, base_dir)
