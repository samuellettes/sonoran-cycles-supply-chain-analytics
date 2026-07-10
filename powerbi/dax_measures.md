# Sonoran Cycles Power BI DAX Measures

## Revenue Measures

```DAX
Booked Revenue =
SUM(sales_order_lines[extended_price])

Fulfilled Revenue =
SUM(sales_order_lines[fulfilled_revenue])

Booked Gross Profit =
SUM(sales_order_lines[gross_profit])

Fulfilled Gross Profit =
SUM(sales_order_lines[fulfilled_gross_profit])

Booked Gross Margin % =
DIVIDE(
    [Booked Gross Profit],
    [Booked Revenue]
)

Fulfilled Gross Margin % =
DIVIDE(
    [Fulfilled Gross Profit],
    [Fulfilled Revenue]
)

Requested Units =
SUM(sales_order_lines[requested_qty])

Fulfilled Units =
SUM(sales_order_lines[fulfilled_qty])

Backordered Units =
SUM(sales_order_lines[backordered_qty])

Service Level =
DIVIDE(
    [Fulfilled Units],
    [Requested Units]
)

Backorder Rate =
DIVIDE(
    [Backordered Units],
    [Requested Units]
)

Sales Orders =
DISTINCTCOUNT(sales_orders[sales_order_id])

Sales Order Lines =
COUNTROWS(sales_order_lines)

Average Order Value =
DIVIDE(
    [Booked Revenue],
    [Sales Orders]
)

Average Selling Price =
DIVIDE(
    [Booked Revenue],
    [Requested Units]
)

Ending On Hand Units =
SUM(inventory_history[on_hand])

Ending Available Units =
SUM(inventory_history[available])

Out of Stock SKUs =
CALCULATE(
    DISTINCTCOUNT(inventory_history[product_id]),
    inventory_history[available] <= 0
)

Average Available Units =
AVERAGE(inventory_history[available])

Purchase Orders =
DISTINCTCOUNT(purchase_orders[purchase_order_id])

Ordered Units =
SUM(purchase_orders[ordered_qty])

Received Units =
SUM(purchase_orders[received_qty])

Open PO Units =
SUMX(
    purchase_orders,
    IF(
        purchase_orders[po_status] = "Open",
        purchase_orders[ordered_qty] - purchase_orders[received_qty],
        0
    )
)

PO Receipt Rate =
DIVIDE(
    [Received Units],
    [Ordered Units]
)

Forecast Quantity =
SUM(forecast_history[forecast_qty])

Actual Quantity =
SUM(forecast_history[actual_qty])

Forecast Error =
SUM(forecast_history[forecast_error])

Absolute Error =
SUM(forecast_history[absolute_error])

Forecast WAPE =
DIVIDE(
    [Absolute Error],
    [Actual Quantity]
)

Forecast Bias % =
DIVIDE(
    [Forecast Error],
    [Actual Quantity]
)

Forecast Accuracy =
1 - [Forecast WAPE]

