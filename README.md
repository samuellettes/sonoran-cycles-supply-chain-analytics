# Sonoran Cycles Supply Chain Analytics

## Project Overview

Sonoran Cycles is a fictional premium bicycle manufacturer used to simulate a realistic supply chain analytics environment.

This project creates an end-to-end analytical workflow for demand planning, inventory management, replenishment, forecasting, SQL analysis, and dashboard design.

The goal is to demonstrate how a supply chain analyst can build and analyze ERP-style data using Python, SQL, SQLite, and Power BI.

---

## Business Scenario

Sonoran Cycles sells premium mountain and gravel bikes through two channels:

- Dealer
- Direct-to-Consumer

The company manages a multi-model bicycle catalog, dealer accounts, finished-goods inventory, supplier replenishment, and monthly demand forecasts.

The business problem is to understand how demand, inventory availability, supplier lead times, and forecast accuracy affect fulfillment performance.

---

## Key Business Questions

This project answers questions such as:

- Which bike models generate the most revenue?
- Which SKUs create the most backorders?
- Which products have the weakest service levels?
- How does Dealer demand compare to DTC demand?
- Which suppliers create the most replenishment exposure?
- Which models are hardest to forecast?
- Where should inventory planning assumptions be adjusted?

---

## Tools Used

- Python
- pandas
- NumPy
- Jupyter Notebook
- SQLite
- SQL
- Git
- Power BI planning documentation

---

## Project Workflow

```text
Master Data
    ↓
Demand Simulation
    ↓
Sales Order Generation
    ↓
Inventory Allocation
    ↓
Purchase Order Replenishment
    ↓
Forecast Generation
    ↓
Analytics Summary Tables
    ↓
SQLite Database
    ↓
SQL Business Analysis
    ↓
Power BI Dashboard Design

## Key Findings

The latest simulation run produced several supply chain planning insights:

- The highest-revenue model was **Romero**, generating **$170,500,841** in booked revenue.
- The weakest model-level service level was **Sabino**, with a service level of **50.7%**.
- The SKU with the highest stockout exposure was **SON-ROM-C-M-IR**, with **884 stockout days**.
- The hardest model to forecast was **Sonoita**, with WAPE of **57.8%**.
- The supplier with the highest open PO exposure was **Merida Industry**, with **3,797 open units**.

These findings demonstrate how demand planning, inventory policy, supplier replenishment, and forecast accuracy interact in a simulated bicycle manufacturing environment.

For a full generated report, see:

```text
reports/executive_insights.md

## Project Outputs

This project generates several reusable outputs:

### Raw Simulation Outputs

- `outputs/sales_orders.csv`
- `outputs/sales_order_lines.csv`
- `outputs/purchase_orders.csv`
- `outputs/inventory_history.csv`
- `outputs/forecast_history.csv`
- `outputs/daily_order_summary.csv`

### Analytics Outputs

- `outputs/analytics/monthly_sales_summary.csv`
- `outputs/analytics/model_performance_summary.csv`
- `outputs/analytics/inventory_kpi_summary.csv`
- `outputs/analytics/forecast_accuracy_by_model.csv`
- `outputs/analytics/supplier_performance_summary.csv`
- `outputs/analytics/daily_kpi_summary.csv`

### Reports

- `reports/project_summary.md`
- `reports/executive_insights.md`

### SQL

- `sql/01_validation_queries.sql`
- `sql/02_business_analysis_queries.sql`

### Power BI Planning

- `powerbi/dashboard_design.md`
- `powerbi/data_model.md`
- `powerbi/dax_measures.md`
- `powerbi/import_checklist.md`
- `powerbi/build_sequence.md`

