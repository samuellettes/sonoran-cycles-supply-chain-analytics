# Sonoran Cycles Executive Insights

## KPI Snapshot

| Metric | Value |
|---|---:|
| Sales Orders | 36,942 |
| Sales Order Lines | 102,608 |
| Purchase Orders | 2,168 |
| Booked Revenue | $659,862,478 |
| Fulfilled Revenue | $416,172,603 |
| Requested Units | 206,636 |
| Fulfilled Units | 130,115 |
| Backordered Units | 76,521 |
| Service Level | 63.0% |
| Backorder Rate | 37.0% |
| Open PO Units | 4,331 |
| Forecast WAPE | 29.4% |
| Forecast Bias | 0.4% |

---

## Key Findings

- The highest-revenue model was **Romero**, generating **$168,392,959** in booked revenue.
- The weakest model-level service level was **Sabino**, with a service level of **50.1%**.
- The SKU with the highest stockout exposure was **SON-SAB-C-M-IR**, with **901 stockout days**.
- The hardest model to forecast was **Sonoita**, with WAPE of **59.3%**.
- The supplier with the highest open PO exposure was **Merida Industry**, with **3,970 open units**.

---

## Planning Implications

The simulation suggests that demand planning should focus on three areas:

1. **High-revenue models with fulfillment risk**  
   Products that drive meaningful revenue but have weak service levels should receive priority in inventory planning.

2. **SKU-level stockout concentration**  
   Stockout days and backordered units help identify where reorder points or target stock levels may be too low.

3. **Forecast accuracy by model and season**  
   Models with high WAPE or consistent bias may need more refined forecasting logic, especially around seasonal demand shifts.

---

## Recommended Actions

- Review reorder points and target stock levels for SKUs with high stockout days.
- Prioritize inventory availability for high-revenue models with below-average service levels.
- Investigate whether forecast bias is concentrated in specific models or months.
- Monitor supplier open PO exposure to understand replenishment timing risk.
- Use the Power BI dashboard to track service level, backorders, supplier exposure, and forecast accuracy over time.

---

## Portfolio Summary

This report was generated from a Python-based supply chain simulation that creates ERP-style sales orders, inventory history, purchase orders, replenishment activity, and forecast history.

The analysis demonstrates how simulated operational data can be transformed into SQL analysis, KPI summaries, and dashboard-ready business insights.
