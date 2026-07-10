# Power BI Dashboard Build Sequence

## Goal

Build the Sonoran Cycles Power BI dashboard in a structured sequence so the report is easy to validate and explain.

---

# Phase 1: Import Data

Import the CSV files from:

- data/
- outputs/

Start with the core model:

## Dimension Tables

- products
- customers
- suppliers
- calendar

## Fact Tables

- sales_orders
- sales_order_lines
- purchase_orders
- inventory_history
- forecast_history
- daily_order_summary

Do not start with every analytics summary table. Add those later only if they simplify specific visuals.

---

# Phase 2: Clean Data Types

In Power Query, confirm all key fields have the correct data type.

## Convert to Date

- calendar[date]
- sales_orders[order_date]
- purchase_orders[order_date]
- purchase_orders[expected_receipt_date]
- purchase_orders[actual_receipt_date]
- inventory_history[snapshot_date]
- forecast_history[forecast_month]
- daily_order_summary[date]

## Convert to Decimal Number

- unit_price
- extended_price
- fulfilled_revenue
- unit_cost
- extended_cost
- fulfilled_cost
- gross_profit
- fulfilled_gross_profit
- forecast_error
- absolute_error

## Convert to Whole Number

- requested_qty
- fulfilled_qty
- backordered_qty
- ordered_qty
- received_qty
- on_hand
- available
- forecast_qty
- actual_qty

---

# Phase 3: Build Relationships

Create relationships in this order:

1. products to sales_order_lines
2. sales_orders to sales_order_lines
3. customers to sales_orders
4. calendar to sales_orders
5. products to inventory_history
6. calendar to inventory_history
7. products to purchase_orders
8. suppliers to purchase_orders
9. calendar to purchase_orders
10. products to forecast_history
11. calendar to forecast_history

Use single-direction filters from dimension tables to fact tables.

---

# Phase 4: Create Core Measures

Create the measures listed in:

powerbi/dax_measures.md

Start with these first:

- Booked Revenue
- Fulfilled Revenue
- Requested Units
- Fulfilled Units
- Backordered Units
- Service Level
- Backorder Rate
- Forecast WAPE
- Forecast Bias %
- Open PO Units

Validate these before creating visuals.

---

# Phase 5: Build Page 1 — Executive Overview

## KPI Cards

- Booked Revenue
- Fulfilled Revenue
- Requested Units
- Fulfilled Units
- Backordered Units
- Service Level
- Forecast WAPE
- Open PO Units

## Visuals

1. Monthly booked revenue trend
2. Revenue by model
3. Service level by model
4. Backordered units by model

## Slicers

- Year
- Sales Channel
- Model Name
- Category

---

# Phase 6: Build Page 2 — Demand & Revenue Analysis

## Visuals

1. Booked Revenue by Model
2. Requested Units by Model
3. Revenue by Sales Channel
4. Dealer Revenue by Region
5. Dealer Tier Performance

## Slicers

- Year
- Month
- Sales Channel
- Region
- Dealer Tier

---

# Phase 7: Build Page 3 — Inventory & Service Level

## Visuals

1. Daily Service Level Trend
2. Daily Backordered Units
3. Out-of-Stock SKUs Over Time
4. Worst SKUs by Backordered Units
5. Worst SKUs by Stockout Days

## Slicers

- Year
- Model Name
- Category
- Size
- Color

---

# Phase 8: Build Page 4 — Forecast & Supplier Performance

## Visuals

1. Forecast WAPE by Model
2. Forecast Bias by Model
3. Forecast Bias by Month
4. Supplier Open PO Units
5. Ordered vs Received Units by Supplier

## Slicers

- Forecast Month
- Model Name
- Category
- Supplier Name

---

# Phase 9: Validate Report Totals

Before polishing the report, compare Power BI totals against the Python and SQL outputs.

Validate:

- Booked Revenue
- Fulfilled Revenue
- Requested Units
- Fulfilled Units
- Backordered Units
- Purchase Orders
- Ordered Units
- Received Units
- Open PO Units
- Forecast WAPE
- Forecast Bias %

If totals do not match, check relationships, date types, and filter context.

---

# Phase 10: Polish the Dashboard

## Formatting

- Use consistent number formatting
- Revenue should be currency
- Percentages should display as percentages
- Units should use whole numbers
- Use clear chart titles
- Avoid unnecessary gridlines
- Keep the report clean and businesslike

## Suggested Visual Style

- Light background
- Dark text
- Muted colors
- Minimal decorative elements
- KPI cards across the top
- Detailed tables lower on the page

---

# Phase 11: Portfolio Write-Up

After the dashboard is built, document:

- Business problem
- Data generation process
- Supply chain simulation logic
- SQL analysis questions
- Dashboard pages
- Key findings
- Recommended planning actions

The dashboard should support the story that Sonoran Cycles needs to balance strong demand, SKU-level inventory availability, supplier replenishment timing, and forecast accuracy.