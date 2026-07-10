# Sonoran Cycles Executive Insights

## KPI Snapshot

| Metric | Value |
|---|---:|
| Sales Orders | 36,991 |
| Sales Order Lines | 102,844 |
| Purchase Orders | 2,157 |
| Booked Revenue | $660,585,998 |
| Fulfilled Revenue | $414,510,738 |
| Requested Units | 207,231 |
| Fulfilled Units | 129,974 |
| Backordered Units | 77,257 |
| Service Level | 62.7% |
| Backorder Rate | 37.3% |
| Open PO Units | 4,042 |
| Forecast WAPE | 29.6% |
| Forecast Bias | 0.1% |

---

## Key Findings

- The highest-revenue model was **Romero**, generating **$170,500,841** in booked revenue.
- The weakest model-level service level was **Sabino**, with a service level of **50.7%**.
- The SKU with the highest stockout exposure was **SON-ROM-C-M-IR**, with **884 stockout days**.
- The hardest model to forecast was **Sonoita**, with WAPE of **57.8%**.
- The supplier with the highest open PO exposure was **Merida Industry**, with **3,797 open units**.

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
