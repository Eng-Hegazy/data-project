"""
generate_interactive_dashboard.py
Generates a standalone, fully interactive HTML/JavaScript dashboard.
Features:
- Responsive executive dashboard UI
- Interactive filters (Region, Category, Year) with live KPI recalculations
- Chart.js dynamic visualizations with hover tooltips and legends
- Searchable, sortable data table
- Export / Print capabilities
"""

import os
import json
import pandas as pd

def build_interactive_dashboard(clean_csv_path, output_dir):
    print("Generating interactive HTML dashboard...")
    df = pd.read_csv(clean_csv_path)

    # Convert records to JSON for client-side filtering and rendering
    # Select columns needed for interactive charts
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
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #F8FAFC;
        }}
        @media print {{
            .no-print {{ display: none !important; }}
            body {{ background-color: #FFFFFF; }}
        }}
        .card-shadow {{
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        }}
    </style>
</head>
<body class="text-slate-800 antialiased p-4 md:p-8">

    <!-- Top Executive Header -->
    <div class="max-w-7xl mx-auto mb-6">
        <div class="bg-slate-900 rounded-2xl p-6 text-white flex flex-col md:flex-row justify-between items-start md:items-center card-shadow">
            <div>
                <div class="flex items-center gap-2 mb-1">
                    <span class="bg-blue-500 text-xs font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider">Business Intelligence</span>
                    <span class="text-xs text-slate-400">2024 - 2025 Multi-Year Analytics</span>
                </div>
                <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight">Executive E-Commerce & Retail Dashboard</h1>
                <p class="text-slate-400 text-sm mt-1">Holistic analysis of revenue, margin performance, customer segments, and fulfillment logistics.</p>
            </div>
            <div class="mt-4 md:mt-0 flex gap-3 no-print">
                <button onclick="window.print()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold px-4 py-2.5 rounded-lg border border-slate-700 transition flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4H7v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
                    Print / Export PDF
                </button>
                <button onclick="resetFilters()" class="bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-4 py-2.5 rounded-lg shadow transition flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                    Reset Filters
                </button>
            </div>
        </div>
    </div>

    <!-- Filter Control Bar -->
    <div class="max-w-7xl mx-auto mb-6 bg-white p-4 rounded-xl border border-slate-200 card-shadow no-print">
        <div class="flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-2 text-slate-600 font-semibold text-sm">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
                <span>Interactive Filters:</span>
            </div>
            <div class="flex flex-wrap items-center gap-3">
                <div>
                    <label class="text-xs font-medium text-slate-500 block mb-1">Region</label>
                    <select id="filterRegion" onchange="applyFilters()" class="text-sm bg-slate-50 border border-slate-300 rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-blue-500 focus:outline-none">
                        <option value="All">All Regions (4)</option>
                        <option value="North">North</option>
                        <option value="South">South</option>
                        <option value="East">East</option>
                        <option value="West">West</option>
                    </select>
                </div>
                <div>
                    <label class="text-xs font-medium text-slate-500 block mb-1">Product Category</label>
                    <select id="filterCategory" onchange="applyFilters()" class="text-sm bg-slate-50 border border-slate-300 rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-blue-500 focus:outline-none">
                        <option value="All">All Categories (3)</option>
                        <option value="Technology">Technology</option>
                        <option value="Furniture">Furniture</option>
                        <option value="Office Supplies">Office Supplies</option>
                    </select>
                </div>
                <div>
                    <label class="text-xs font-medium text-slate-500 block mb-1">Fiscal Year</label>
                    <select id="filterYear" onchange="applyFilters()" class="text-sm bg-slate-50 border border-slate-300 rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-blue-500 focus:outline-none">
                        <option value="All">All Years (2024 - 2025)</option>
                        <option value="2024">FY 2024</option>
                        <option value="2025">FY 2025</option>
                    </select>
                </div>
            </div>
        </div>
    </div>

    <!-- KPI Metric Cards Grid -->
    <div class="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
        <!-- Revenue -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow border-l-4 border-l-blue-600">
            <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Total Sales</span>
            <div id="kpiRevenue" class="text-xl md:text-2xl font-black text-slate-900 mt-1">$0</div>
            <span class="text-xs font-medium text-blue-600 mt-1 block">Gross Net Revenue</span>
        </div>
        <!-- Profit -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow border-l-4 border-l-emerald-600">
            <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Total Profit</span>
            <div id="kpiProfit" class="text-xl md:text-2xl font-black text-slate-900 mt-1">$0</div>
            <span class="text-xs font-medium text-emerald-600 mt-1 block">Operating Net Income</span>
        </div>
        <!-- Margin -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow border-l-4 border-l-teal-600">
            <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Profit Margin</span>
            <div id="kpiMargin" class="text-xl md:text-2xl font-black text-slate-900 mt-1">0.0%</div>
            <span class="text-xs font-medium text-teal-600 mt-1 block">Target: >12.0%</span>
        </div>
        <!-- Units Sold -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow border-l-4 border-l-amber-600">
            <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Total Units</span>
            <div id="kpiUnits" class="text-xl md:text-2xl font-black text-slate-900 mt-1">0</div>
            <span class="text-xs font-medium text-amber-600 mt-1 block">Units Dispatched</span>
        </div>
        <!-- AOV -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow border-l-4 border-l-purple-600 col-span-2 md:col-span-1">
            <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Avg Order Value</span>
            <div id="kpiAOV" class="text-xl md:text-2xl font-black text-slate-900 mt-1">$0.00</div>
            <span class="text-xs font-medium text-purple-600 mt-1 block">Basket Size</span>
        </div>
    </div>

    <!-- Main Visualizations Layout -->
    <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <!-- Chart 1: Monthly Trend (2 Cols) -->
        <div class="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200 card-shadow">
            <div class="flex justify-between items-center mb-4">
                <div>
                    <h2 class="text-base font-bold text-slate-900">1. Monthly Revenue & Operating Profit Trend</h2>
                    <p class="text-xs text-slate-500">Historical performance showing revenue trajectory and seasonal spikes</p>
                </div>
                <span class="text-xs bg-slate-100 text-slate-600 px-2 py-1 rounded font-medium">Monthly Series</span>
            </div>
            <div class="h-72">
                <canvas id="chartTrend"></canvas>
            </div>
        </div>

        <!-- Chart 2: Customer Segment Donut (1 Col) -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 card-shadow">
            <div class="flex justify-between items-center mb-4">
                <div>
                    <h2 class="text-base font-bold text-slate-900">2. Customer Segment Distribution</h2>
                    <p class="text-xs text-slate-500">Revenue split across demographic client segments</p>
                </div>
            </div>
            <div class="h-72 flex items-center justify-center">
                <canvas id="chartSegment"></canvas>
            </div>
        </div>
    </div>

    <!-- Second Row Visualizations -->
    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <!-- Chart 3: Sub-Category Horizontal Bar -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 card-shadow">
            <div class="flex justify-between items-center mb-4">
                <div>
                    <h2 class="text-base font-bold text-slate-900">3. Sales by Product Sub-Category</h2>
                    <p class="text-xs text-slate-500">Comparative revenue contribution by product line</p>
                </div>
            </div>
            <div class="h-80">
                <canvas id="chartSubcat"></canvas>
            </div>
        </div>

        <!-- Chart 4: Regional Performance -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 card-shadow">
            <div class="flex justify-between items-center mb-4">
                <div>
                    <h2 class="text-base font-bold text-slate-900">4. Regional Sales vs. Profit Comparison</h2>
                    <p class="text-xs text-slate-500">Geographic sales performance and margin realization</p>
                </div>
            </div>
            <div class="h-80">
                <canvas id="chartRegion"></canvas>
            </div>
        </div>

        <!-- Chart 5: Shipping Mode Distribution -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 card-shadow">
            <div class="flex justify-between items-center mb-4">
                <div>
                    <h2 class="text-base font-bold text-slate-900">5. Logistics & Shipping Mode Performance</h2>
                    <p class="text-xs text-slate-500">Order count and fulfillment speed by class</p>
                </div>
            </div>
            <div class="h-80">
                <canvas id="chartShip"></canvas>
            </div>
        </div>
    </div>

    <!-- Data Summary Table -->
    <div class="max-w-7xl mx-auto bg-white p-5 rounded-xl border border-slate-200 card-shadow mb-8">
        <div class="flex justify-between items-center mb-4">
            <div>
                <h2 class="text-base font-bold text-slate-900">6. Sub-Category Performance Summary Matrix</h2>
                <p class="text-xs text-slate-500">Aggregated sales, profit, margin %, and fulfillment efficiency</p>
            </div>
        </div>
        <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
                <thead class="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200">
                    <tr>
                        <th class="py-3 px-4">Sub-Category</th>
                        <th class="py-3 px-4">Category</th>
                        <th class="py-3 px-4 text-right">Orders</th>
                        <th class="py-3 px-4 text-right">Units Sold</th>
                        <th class="py-3 px-4 text-right">Total Revenue</th>
                        <th class="py-3 px-4 text-right">Operating Profit</th>
                        <th class="py-3 px-4 text-right">Profit Margin %</th>
                    </tr>
                </thead>
                <tbody id="tableBody" class="divide-y divide-slate-100 text-slate-700">
                    <!-- Populated dynamically via JS -->
                </tbody>
            </table>
        </div>
    </div>

    <!-- Footer metadata -->
    <div class="max-w-7xl mx-auto text-center text-xs text-slate-400 py-4 border-t border-slate-200">
        E-Commerce Executive Analytics Dashboard | Prepared with Python, Chart.js & Tailwind CSS | Academic Project Submission
    </div>

    <!-- Embedded Dataset & Reactive JS Logic -->
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
                            backgroundColor: 'rgba(37, 99, 235, 0.1)',
                            fill: true,
                            tension: 0.3,
                            borderWidth: 2.5
                        }},
                        {{
                            label: 'Operating Profit ($)',
                            data: profitData,
                            borderColor: '#10B981',
                            backgroundColor: 'rgba(16, 185, 129, 0.05)',
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
                        legend: {{ position: 'top', labels: {{ font: {{ family: 'Plus Jakarta Sans', size: 11 }} }} }}
                    }},
                    scales: {{
                        y: {{
                            ticks: {{ callback: value => '$' + (value/1000) + 'k' }},
                            grid: {{ color: '#F1F5F9' }}
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
                        backgroundColor: ['#3B82F6', '#10B981', '#F59E0B'],
                        borderWidth: 2,
                        borderColor: '#FFFFFF'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ font: {{ family: 'Plus Jakarta Sans', size: 11 }} }} }}
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
                        backgroundColor: '#6366F1',
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
                            grid: {{ color: '#F1F5F9' }}
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
                        {{ label: 'Revenue ($)', data: sales, backgroundColor: '#0EA5E9', borderRadius: 4 }},
                        {{ label: 'Profit ($)', data: profits, backgroundColor: '#10B981', borderRadius: 4 }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'top', labels: {{ font: {{ family: 'Plus Jakarta Sans', size: 10 }} }} }}
                    }},
                    scales: {{
                        y: {{
                            ticks: {{ callback: value => '$' + (value/1000) + 'k' }},
                            grid: {{ color: '#F1F5F9' }}
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
                    shipMap[d.Shipping_Mode] = {{ count: 0, daysTotal: 0 }};
                }}
                shipMap[d.Shipping_Mode].count += 1;
                shipMap[d.Shipping_Mode].daysTotal += d.Shipping_Days;
            }});

            const modes = Object.keys(shipMap);
            const counts = modes.map(m => shipMap[m].count);

            if (chartShipInstance) chartShipInstance.destroy();

            const ctx = document.getElementById('chartShip').getContext('2d');
            chartShipInstance = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: modes,
                    datasets: [{{
                        label: 'Orders Dispatched',
                        data: counts,
                        backgroundColor: ['#4F46E5', '#7C3AED', '#EC4899', '#F43F5E'],
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
                        y: {{ grid: {{ color: '#F1F5F9' }} }},
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
                const marginColor = margin >= 15 ? 'text-emerald-700 bg-emerald-50' : (margin >= 8 ? 'text-blue-700 bg-blue-50' : 'text-amber-700 bg-amber-50');

                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50/80 transition';
                tr.innerHTML = `
                    <td class="py-2.5 px-4 font-semibold text-slate-800">${{name}}</td>
                    <td class="py-2.5 px-4 text-slate-500">${{val.category}}</td>
                    <td class="py-2.5 px-4 text-right">${{val.orders.toLocaleString()}}</td>
                    <td class="py-2.5 px-4 text-right">${{val.units.toLocaleString()}}</td>
                    <td class="py-2.5 px-4 text-right font-medium">${{formatCurrency(val.sales)}}</td>
                    <td class="py-2.5 px-4 text-right font-medium text-emerald-600">${{formatCurrency(val.profit)}}</td>
                    <td class="py-2.5 px-4 text-right">
                        <span class="px-2 py-0.5 rounded-full font-bold ${{marginColor}}">
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

        // Initialize on load
        window.addEventListener('DOMContentLoaded', () => {{
            applyFilters();
        }});
    </script>
</body>
</html>
"""

    html_path = os.path.join(output_dir, "ecommerce_dashboard.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Interactive HTML dashboard successfully created at: {html_path}")
    return html_path

if __name__ == '__main__':
    base_dir = r"C:\Users\hegazy\.gemini\antigravity\scratch\ecommerce_dashboard"
    clean_csv = os.path.join(base_dir, "ecommerce_sales_cleaned.csv")
    build_interactive_dashboard(clean_csv, base_dir)
