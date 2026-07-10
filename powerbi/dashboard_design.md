# Sonoran Cycles Power BI Dashboard Design

## Dashboard Objective

This dashboard analyzes the simulated supply chain performance of Sonoran Cycles, a fictional premium bicycle manufacturer.

The report focuses on:

- Demand and revenue performance
- Dealer vs DTC channel mix
- Inventory availability
- Service level and backorders
- Supplier replenishment exposure
- Forecast accuracy and bias

The goal is to demonstrate how a supply chain analyst can use Python-generated ERP-style data, SQL analysis, and Power BI dashboards to identify planning risks and recommend operational improvements.

---

# Report Pages

## Page 1: Executive Overview

### Purpose

Provide a high-level view of business performance across revenue, demand, fulfillment, inventory, and forecast accuracy.

### Key Questions

- How much revenue was booked?
- How much demand was fulfilled?
- What is the overall service level?
- How many units were backordered?
- Which models generated the most revenue?
- Which models had fulfillment issues?

### KPI Cards

- Booked Revenue
- Fulfilled Revenue
- Requested Units
- Fulfilled Units
- Backordered Units
- Service Level
- Forecast WAPE
- Open PO Units

### Visuals

1. Monthly Booked Revenue Trend  
   - Axis: Month
   - Values: Booked Revenue
   - Legend: Sales Channel

2. Revenue by Model  
   - Axis: Model Name
   - Values: Booked Revenue

3. Service Level by Model  
   - Axis: Model Name
   - Values: Service Level

4. Backordered Units by Model  
   - Axis: Model Name
   - Values: Backordered Units

### Recommended Slicers

- Year
- Sales Channel
- Model Name
- Category

---

## Page 2: Demand & Revenue Analysis

### Purpose

Explain where demand and revenue are coming from across models, channels, dealer tiers, and regions.

### Key Questions

- Which models drive the most revenue?
- How does Dealer demand compare to DTC demand?
- Which regions generate the most dealer revenue?
- Which dealer tiers are most important?
- Are high-volume channels also profitable?

### Visuals

1. Booked Revenue by Model  
   - Axis: Model Name
   - Values: Booked Revenue

2. Requested Units by Model  
   - Axis: Model Name
   - Values: Requested Units

3. Revenue by Sales Channel  
   - Axis: Sales Channel
   - Values: Booked Revenue

4. Dealer Revenue by Region  
   - Axis: Region
   - Values: Booked Revenue

5. Dealer Tier Performance  
   - Axis: Dealer Tier
   - Values: Booked Revenue, Requested Units

### Recommended Slicers

- Year
- Month
- Sales Channel
- Region
- Dealer Tier

---

## Page 3: Inventory & Service Level

### Purpose

Identify fulfillment problems, inventory constraints, backorders, and SKU-level availability issues.

### Key Questions

- When did service level decline?
- Which SKUs had the most backorders?
- Which SKUs had the most stockout days?
- Did inventory availability keep pace with demand?
- Were backorders concentrated in a few SKUs or spread across the catalog?

### Visuals

1. Daily Service Level Trend  
   - Axis: Date
   - Values: Service Level

2. Daily Backordered Units  
   - Axis: Date
   - Values: Backordered Units

3. Out-of-Stock SKUs Over Time  
   - Axis: Date
   - Values: Out-of-Stock SKUs

4. Worst SKUs by Backordered Units  
   - Axis: SKU
   - Values: Backordered Units

5. Worst SKUs by Stockout Days  
   - Axis: SKU
   - Values: Stockout Days

### Recommended Slicers

- Year
- Model Name
- Category
- Size
- Color

---

## Page 4: Forecast & Supplier Performance

### Purpose

Evaluate forecast quality and supplier replenishment exposure.

### Key Questions

- Which models are hardest to forecast?
- Is the forecast biased high or low?
- Are certain months consistently over-forecast or under-forecast?
- Which suppliers have the most open purchase order exposure?
- How much replenishment volume has been ordered and received?

### Visuals

1. Forecast WAPE by Model  
   - Axis: Model Name
   - Values: WAPE

2. Forecast Bias by Model  
   - Axis: Model Name
   - Values: Bias %

3. Forecast Bias by Month  
   - Axis: Forecast Month
   - Values: Bias %

4. Supplier Open PO Units  
   - Axis: Supplier Name
   - Values: Open Units

5. Ordered vs Received Units by Supplier  
   - Axis: Supplier Name
   - Values: Ordered Units, Received Units

### Recommended Slicers

- Forecast Month
- Model Name
- Category
- Supplier Name

---

# Dashboard Design Notes

## Visual Style

The dashboard should feel like an executive supply chain report rather than a marketing presentation.

Recommended style:

- Clean white or light gray background
- Dark text
- Minimal decorative elements
- Consistent chart titles
- KPI cards across the top of each page
- Tables only where detail is necessary

## Business Framing

The dashboard should support this portfolio narrative:

Sonoran Cycles has strong demand across its premium bicycle portfolio, but fulfillment performance depends on SKU-level inventory availability, supplier lead times, and forecast quality. The dashboard helps identify where demand exceeds supply and where planning assumptions should be adjusted.

## Primary KPIs

- Booked Revenue
- Fulfilled Revenue
- Requested Units
- Fulfilled Units
- Backordered Units
- Service Level
- Backorder Rate
- Forecast WAPE
- Forecast Bias
- Open PO Units
- Stockout Days