# Sonoran Cycles Power BI Data Model

## Recommended Data Source

Use the project CSV files as the Power BI data source.

SQLite is used for SQL analysis, but CSV files are easier to manage in Power BI.

---

# Tables to Load

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

## Analytics Tables

- monthly_sales_summary
- model_performance_summary
- inventory_kpi_summary
- forecast_accuracy_by_model
- supplier_performance_summary
- daily_kpi_summary

---

# Recommended Relationships

## Sales Model

products[product_id]  
→ sales_order_lines[product_id]

sales_orders[sales_order_id]  
→ sales_order_lines[sales_order_id]

customers[customer_id]  
→ sales_orders[customer_id]

calendar[date]  
→ sales_orders[order_date]

---

## Purchasing Model

products[product_id]  
→ purchase_orders[product_id]

suppliers[supplier_id]  
→ purchase_orders[supplier_id]

calendar[date]  
→ purchase_orders[order_date]

---

## Inventory Model

products[product_id]  
→ inventory_history[product_id]

calendar[date]  
→ inventory_history[snapshot_date]

---

## Forecast Model

products[product_id]  
→ forecast_history[product_id]

calendar[date]  
→ forecast_history[forecast_month]

---

# Notes

Power BI may require converting date columns to Date type after import.

Important date columns:

- calendar[date]
- sales_orders[order_date]
- purchase_orders[order_date]
- purchase_orders[expected_receipt_date]
- purchase_orders[actual_receipt_date]
- inventory_history[snapshot_date]
- forecast_history[forecast_month]

---

# Recommended Model Structure

Use a star-schema style model where possible.

The main analytical grain is:

- sales_order_lines: one row per sales order line
- inventory_history: one row per product per day
- purchase_orders: one row per purchase order
- forecast_history: one row per product per forecast month

Avoid building visuals directly from too many disconnected summary tables unless the summary table is specifically designed for that page.

For most interactive dashboard pages, prefer fact tables plus dimensions.