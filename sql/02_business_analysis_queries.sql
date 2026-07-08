-- 02_business_analysis_queries.sql
--
-- Business analysis queries for the Sonoran Cycles SQLite database.
--
-- These queries investigate revenue, demand, fulfillment, inventory,
-- supplier exposure, and forecast accuracy.


-- =========================================================
-- 1. Revenue and demand by bike model
-- =========================================================

SELECT
    model_name,
    category,
    SUM(requested_qty) AS requested_units,
    SUM(fulfilled_qty) AS fulfilled_units,
    SUM(backordered_qty) AS backordered_units,
    ROUND(SUM(extended_price), 2) AS booked_revenue,
    ROUND(SUM(fulfilled_revenue), 2) AS fulfilled_revenue,
    ROUND(SUM(gross_profit), 2) AS booked_gross_profit,
    ROUND(SUM(fulfilled_gross_profit), 2) AS fulfilled_gross_profit,
    ROUND(
        CAST(SUM(fulfilled_qty) AS FLOAT) / NULLIF(SUM(requested_qty), 0),
        3
    ) AS service_level,
    ROUND(
        CAST(SUM(backordered_qty) AS FLOAT) / NULLIF(SUM(requested_qty), 0),
        3
    ) AS backorder_rate
FROM sales_order_lines
GROUP BY
    model_name,
    category
ORDER BY
    booked_revenue DESC;


-- =========================================================
-- 2. Monthly revenue and demand trend
-- =========================================================

SELECT
    substr(so.order_date, 1, 7) AS order_month,
    so.sales_channel,
    COUNT(DISTINCT so.sales_order_id) AS sales_orders,
    SUM(sol.requested_qty) AS requested_units,
    SUM(sol.fulfilled_qty) AS fulfilled_units,
    SUM(sol.backordered_qty) AS backordered_units,
    ROUND(SUM(sol.extended_price), 2) AS booked_revenue,
    ROUND(SUM(sol.fulfilled_revenue), 2) AS fulfilled_revenue,
    ROUND(
        CAST(SUM(sol.fulfilled_qty) AS FLOAT) / NULLIF(SUM(sol.requested_qty), 0),
        3
    ) AS service_level
FROM sales_orders so
JOIN sales_order_lines sol
    ON so.sales_order_id = sol.sales_order_id
GROUP BY
    substr(so.order_date, 1, 7),
    so.sales_channel
ORDER BY
    order_month,
    so.sales_channel;


-- =========================================================
-- 3. Dealer vs DTC channel performance
-- =========================================================

SELECT
    so.sales_channel,
    COUNT(DISTINCT so.sales_order_id) AS sales_orders,
    COUNT(DISTINCT so.customer_id) AS customers,
    SUM(sol.requested_qty) AS requested_units,
    SUM(sol.fulfilled_qty) AS fulfilled_units,
    SUM(sol.backordered_qty) AS backordered_units,
    ROUND(SUM(sol.extended_price), 2) AS booked_revenue,
    ROUND(SUM(sol.fulfilled_revenue), 2) AS fulfilled_revenue,
    ROUND(AVG(sol.unit_price), 2) AS average_unit_price,
    ROUND(
        CAST(SUM(sol.fulfilled_qty) AS FLOAT) / NULLIF(SUM(sol.requested_qty), 0),
        3
    ) AS service_level
FROM sales_orders so
JOIN sales_order_lines sol
    ON so.sales_order_id = sol.sales_order_id
GROUP BY
    so.sales_channel
ORDER BY
    booked_revenue DESC;


-- =========================================================
-- 4. Regional dealer demand and revenue
-- =========================================================

SELECT
    c.region,
    c.state,
    COUNT(DISTINCT so.sales_order_id) AS sales_orders,
    COUNT(DISTINCT so.customer_id) AS customers,
    SUM(sol.requested_qty) AS requested_units,
    ROUND(SUM(sol.extended_price), 2) AS booked_revenue,
    ROUND(SUM(sol.fulfilled_revenue), 2) AS fulfilled_revenue,
    ROUND(
        CAST(SUM(sol.fulfilled_qty) AS FLOAT) / NULLIF(SUM(sol.requested_qty), 0),
        3
    ) AS service_level
FROM sales_orders so
JOIN customers c
    ON so.customer_id = c.customer_id
JOIN sales_order_lines sol
    ON so.sales_order_id = sol.sales_order_id
WHERE so.sales_channel = 'Dealer'
GROUP BY
    c.region,
    c.state
ORDER BY
    booked_revenue DESC;


-- =========================================================
-- 5. Worst SKUs by backordered units
-- =========================================================

SELECT
    sol.product_id,
    sol.sku,
    sol.model_name,
    sol.category,
    sol.size,
    sol.color,
    SUM(sol.requested_qty) AS requested_units,
    SUM(sol.fulfilled_qty) AS fulfilled_units,
    SUM(sol.backordered_qty) AS backordered_units,
    ROUND(SUM(sol.extended_price), 2) AS booked_revenue,
    ROUND(
        CAST(SUM(sol.backordered_qty) AS FLOAT) / NULLIF(SUM(sol.requested_qty), 0),
        3
    ) AS backorder_rate
FROM sales_order_lines sol
GROUP BY
    sol.product_id,
    sol.sku,
    sol.model_name,
    sol.category,
    sol.size,
    sol.color
HAVING
    SUM(sol.requested_qty) > 0
ORDER BY
    backordered_units DESC,
    backorder_rate DESC
LIMIT 25;


-- =========================================================
-- 6. Worst SKUs by stockout days
-- =========================================================

SELECT
    product_id,
    sku,
    model_name,
    category,
    size,
    color,
    ROUND(average_available, 2) AS average_available,
    minimum_available,
    ending_available,
    stockout_days,
    ROUND(stockout_rate, 3) AS stockout_rate
FROM inventory_kpi_summary
ORDER BY
    stockout_days DESC,
    stockout_rate DESC,
    average_available ASC
LIMIT 25;


-- =========================================================
-- 7. Supplier purchase order exposure
-- =========================================================

SELECT
    supplier_id,
    supplier_name,
    purchase_orders,
    open_purchase_orders,
    received_purchase_orders,
    ordered_units,
    received_units,
    open_units,
    ROUND(average_lead_time_days, 1) AS average_lead_time_days,
    ROUND(receipt_rate, 3) AS receipt_rate
FROM supplier_performance_summary
ORDER BY
    open_units DESC,
    ordered_units DESC;


-- =========================================================
-- 8. Forecast accuracy by model
-- =========================================================

SELECT
    model_name,
    category,
    actual_qty,
    forecast_qty,
    absolute_error,
    forecast_error,
    ROUND(wape, 3) AS wape,
    ROUND(bias_pct, 3) AS bias_pct,
    ROUND(forecast_accuracy, 3) AS forecast_accuracy
FROM forecast_accuracy_by_model
ORDER BY
    wape DESC;


-- =========================================================
-- 9. Forecast bias by month
-- =========================================================

SELECT
    forecast_month,
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
    forecast_month
ORDER BY
    forecast_month;


-- =========================================================
-- 10. Products with high demand but weak service level
-- =========================================================

WITH product_performance AS (
    SELECT
        sol.product_id,
        sol.sku,
        sol.model_name,
        sol.category,
        sol.size,
        sol.color,
        SUM(sol.requested_qty) AS requested_units,
        SUM(sol.fulfilled_qty) AS fulfilled_units,
        SUM(sol.backordered_qty) AS backordered_units,
        ROUND(SUM(sol.extended_price), 2) AS booked_revenue,
        ROUND(
            CAST(SUM(sol.fulfilled_qty) AS FLOAT) / NULLIF(SUM(sol.requested_qty), 0),
            3
        ) AS service_level
    FROM sales_order_lines sol
    GROUP BY
        sol.product_id,
        sol.sku,
        sol.model_name,
        sol.category,
        sol.size,
        sol.color
)

SELECT
    product_id,
    sku,
    model_name,
    category,
    size,
    color,
    requested_units,
    fulfilled_units,
    backordered_units,
    booked_revenue,
    service_level
FROM product_performance
WHERE
    requested_units >= 50
    AND service_level < 0.90
ORDER BY
    booked_revenue DESC,
    service_level ASC;


-- =========================================================
-- 11. Monthly service level and backorder trend
-- =========================================================

SELECT
    date AS summary_date,
    sales_orders,
    requested_units,
    fulfilled_units,
    backordered_units,
    ROUND(service_level, 3) AS service_level,
    ROUND(backorder_rate, 3) AS backorder_rate,
    purchase_orders_created,
    purchase_units_ordered,
    purchase_orders_received,
    purchase_units_received,
    total_on_hand_units,
    out_of_stock_skus
FROM daily_kpi_summary
ORDER BY
    summary_date;


-- =========================================================
-- 12. Dealer tier performance
-- =========================================================

SELECT
    c.dealer_tier,
    COUNT(DISTINCT so.customer_id) AS customers,
    COUNT(DISTINCT so.sales_order_id) AS sales_orders,
    SUM(sol.requested_qty) AS requested_units,
    ROUND(SUM(sol.extended_price), 2) AS booked_revenue,
    ROUND(SUM(sol.fulfilled_revenue), 2) AS fulfilled_revenue,
    ROUND(
        CAST(SUM(sol.fulfilled_qty) AS FLOAT) / NULLIF(SUM(sol.requested_qty), 0),
        3
    ) AS service_level
FROM sales_orders so
JOIN customers c
    ON so.customer_id = c.customer_id
JOIN sales_order_lines sol
    ON so.sales_order_id = sol.sales_order_id
WHERE
    so.sales_channel = 'Dealer'
GROUP BY
    c.dealer_tier
ORDER BY
    booked_revenue DESC;