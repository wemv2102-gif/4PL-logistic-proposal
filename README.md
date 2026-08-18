# 🚌 4PL Logistics Optimization: Monetizing Idle Capacity in Buses

**Role:** Data Analyst & Logistics Strategist
**Tools Used:** Tableau, SQL, Excel / Google Sheets

## 📌 Project Overview
Commercial and operational feasibility analysis to open a new B2B/B2C parcel delivery business line for an interregional transport company. The core objective was to monetize the idle space in bus luggage compartments while generating the lowest possible operational friction and fixed investment (near-zero CapEx).

## 🛠️ Methodology & Data Approach
1. **Market Research (Public Data):** Analyzed consumer complaint reports from SERNAC (Chile's National Consumer Service), identifying delivery delays as the primary pain point in regional e-commerce. Buses, with their fixed and strict itineraries, resolve this issue by guaranteeing punctuality on the trunk network.
2. **Data Modeling:** Structured a simulated dataset cross-referencing B2B volume rates, local operational costs, and geographic demand.
3. **Logistics Model Analysis:** Compared the profitability of a 3PL model (in-house operation, high friction) versus a 4PL model (integrator with local alliances, low friction).

## 📊 Repository Files
* `kargo_simulation_dataset.csv`: Sample of the structured data used to calculate profitability per route.
* `cost_margin_analysis.sql`: SQL queries used to aggregate 1st Mile, Trunk, and Last Mile costs, and to calculate the net margin by client type (Retail vs. SME).
* `Operational_Dashboard.png`: Final visualization developed in Tableau.
* `Executive_Presentation.pdf`: Slide deck summarizing the business case.

## 📈 Key Results (4PL Model)
Following the data simulation and dashboard analysis, the 4PL integrator model proved to be the optimal path:
* **Projected Revenue:** $130,207,701 CLP
* **Net Margin:** $51,305,530 CLP
* **Global Operating Margin:** **39.40%**
* **Strategic Decision:** Yielding a portion of the unit margin to local operators at the destination eliminates the financial risk of physical infrastructure, allowing for immediate scalability.

## 🚀 Recommendations & Roadmap
1. Launch a controlled pilot on high-margin trunk routes (Antofagasta, La Serena, Valparaíso).
2. Structure volume-based pricing tiers for Retail clients.
3. Execute B2B collection and delivery contracts with Last-Mile couriers at the destinations.
