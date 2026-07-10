# Power BI Import Checklist

## Goal

Import the Sonoran Cycles CSV outputs into Power BI and build a clean analytical model for supply chain dashboarding.

---

# Source Files to Import

## Dimension Tables

Load these from the `data/` folder:

- data/products.csv
- data/customers.csv
- data/suppliers.csv
- data/calendar.csv

## Fact Tables

Load these from the `outputs/` folder:

- outputs/sales_orders.csv
- outputs/sales_order_lines.csv
- outputs/purchase_orders.csv
- outputs/inventory_history.csv
- outputs/forecast_history.csv
- outputs/daily_order_summary.csv

## Optional Analytics Tables

Load these only if useful for validation or simplified visuals:

- outputs/analytics/monthly_sales_summary.csv
- outputs/analytics/model_performance_summary.csv
- outputs/analytics/inventory_kpi_summary.csv
- outputs/analytics/forecast_accuracy_by_model.csv
- outputs/analytics/supplier_performance_summary.csv
- outputs/analytics/daily_kpi_summary.csv

For the main report model, prefer the raw fact tables plus dimensions.

---

# Required Data Type Checks

## Date Fields

Convert these to Date type:

- calendar[date]
- sales_orders[order_date]
- purchase_orders[order_date]
- purchase_orders[expected_receipt_date]
- purchase_orders[actual_receipt_date]
- inventory_history[snapshot_date]
- forecast_history[forecast_month]
- daily_order_summary[date]

## Text Fields

Confirm these are Text type:

- product_id
- sku
- sales_order_id
- purchase_order_id
- customer_id
- supplier_id
- model_name
- category
- sales_channel
- dealer_tier
- region
- state
- po_status

## Numeric Fields

Confirm these are Whole Number or Decimal Number:

- requested_qty
- fulfilled_qty
- backordered_qty
- unit_price
- extended_price
- fulfilled_revenue
- gross_profit
- fulfilled_gross_profit
- ordered_qty
- received_qty
- on_hand
- available
- forecast_qty
- actual_qty
- absolute_error
- forecast_error

---

# Recommended Relationships

## Sales

products[product_id] → sales_order_lines[product_id]

sales_orders[sales_order_id] → sales_order_lines[sales_order_id]

customers[customer_id] → sales_orders[customer_id]

calendar[date] → sales_orders[order_date]

## Purchasing

products[product_id] → purchase_orders[product_id]

suppliers[supplier_id] → purchase_orders[supplier_id]

calendar[date] → purchase_orders[order_date]

## Inventory

products[product_id] → inventory_history[product_id]

calendar[date] → inventory_history[snapshot_date]

## Forecast

products[product_id] → forecast_history[product_id]

calendar[date] → forecast_history[forecast_month]

---

# Relationship Notes

Use one-to-many relationships from dimensions to facts.

Recommended filter direction:

- Single direction from dimension tables to fact tables
- Avoid bidirectional filters unless necessary
- Keep products, customers, suppliers, and calendar as clean dimension tables

---

# Import Validation Checks

After loading data, validate these totals against the Python/SQL outputs:

## Sales

- Total booked revenue
- Total fulfilled revenue
- Total requested units
- Total fulfilled units
- Total backordered units

## Inventory

- Total inventory history rows
- Out-of-stock SKU counts by date
- Ending inventory by SKU

## Purchasing

- Total purchase orders
- Ordered units
- Received units
- Open PO units

## Forecast

- Total actual quantity
- Total forecast quantity
- Total absolute error
- Forecast WAPE
- Forecast bias