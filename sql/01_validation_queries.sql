-- 01_validation_queries.sql
--
-- Validation and starter analysis queries for the
-- Sonoran Cycles SQLite database.

-- Row counts by key tables
SELECT 'products' AS table_name, COUNT(*) AS row_count FROM products
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'suppliers', COUNT(*) FROM suppliers
UNION ALL
SELECT 'sales_orders', COUNT(*) FROM sales_orders
UNION ALL
SELECT 'sales_order_lines', COUNT(*) FROM sales_order_lines
UNION ALL
SELECT 'purchase_orders', COUNT(*) FROM purchase_orders
UNION ALL
SELECT 'inventory_history', COUNT(*) FROM inventory_history
UNION ALL
SELECT 'forecast_history', COUNT(*) FROM forecast_history;


-- Revenue and service level by model
SELECT
    model_name,
    category,
    SUM(requested_qty) AS requested_units,
    SUM(fulfilled_qty) AS fulfilled_units,
    SUM(backordered_qty) AS backordered_units,
    ROUND(SUM(extended_price), 2) AS booked_revenue,
    ROUND(SUM(fulfilled_revenue), 2) AS fulfilled_revenue,
    ROUND(
        CAST(SUM(fulfilled_qty) AS FLOAT) / NULLIF(SUM(requested_qty), 0),
        3
    ) AS service_level
FROM sales_order_lines
GROUP BY
    model_name,
    category
ORDER BY
    booked_revenue DESC;


-- Monthly sales trend
SELECT
    substr(order_date, 1, 7) AS order_month,
    sales_channel,
    COUNT(DISTINCT sales_order_id) AS sales_orders,
    ROUND(SUM(order_total), 2) AS booked_revenue
FROM sales_orders
GROUP BY
    substr(order_date, 1, 7),
    sales_channel
ORDER BY
    order_month,
    sales_channel;


-- Forecast accuracy by model
SELECT
    model_name,
    category,
    SUM(actual_qty) AS actual_qty,
    SUM(forecast_qty) AS forecast_qty,
    SUM(absolute_error) AS absolute_error,
    SUM(forecast_error) AS forecast_error,
    ROUND(
        CAST(SUM(absolute_error) AS FLOAT) / NULLIF(SUM(actual_qty), 0),
        3
    ) AS wape,
    ROUND(
        CAST(SUM(forecast_error) AS FLOAT) / NULLIF(SUM(actual_qty), 0),
        3
    ) AS bias_pct
FROM forecast_history
GROUP BY
    model_name,
    category
ORDER BY
    wape DESC;


-- Supplier purchase order exposure
SELECT
    supplier_name,
    COUNT(DISTINCT purchase_order_id) AS purchase_orders,
    SUM(ordered_qty) AS ordered_units,
    SUM(received_qty) AS received_units,
    SUM(
        CASE
            WHEN po_status = 'Open'
            THEN ordered_qty - received_qty
            ELSE 0
        END
    ) AS open_units
FROM purchase_orders
GROUP BY
    supplier_name
ORDER BY
    ordered_units DESC;