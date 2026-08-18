/* =================================================================================
   FILE: cost_margin_analysis.sql
   PROJECT: 4PL Logistics Optimization - Idle Capacity Monetization
   AUTHOR: Williams Moreno
   
   DESCRIPTION:
   This script contains the core SQL queries used to evaluate the commercial 
   feasibility of the 4PL logistics model. It calculates the operating margins 
   by destination, analyzes the cost structure by client segment (Retail vs. SME), 
   and identifies the top routes for the initial pilot phase.
================================================================================= */

-- ---------------------------------------------------------------------------------
-- QUERY 1: Overall Profitability & Operating Margin by Destination City
-- Purpose: Calculate total revenue, costs, and net margin % to validate 
-- which regional routes are financially viable for the 4PL model.
-- ---------------------------------------------------------------------------------

WITH CityFinancials AS (
    SELECT 
        `Destination`,
        `Type of client`,
        COUNT(id_envio) AS total_shipments,
        SUM(Fee) AS total_revenue,
        SUM(`Total operational cost`) AS total_cost
    FROM 
        `project-edebec60-1723-4381-90f.dataset_kupos.datasetv3`
    GROUP BY 
        `Destination`, 
        `Type of client`
)
SELECT 
    `Destination`,
    SUM(total_shipments) AS total_shipments,
    SUM(total_revenue) AS total_revenue,
    SUM(total_cost) AS total_cost,
    (SUM(total_revenue) - SUM(total_cost)) AS net_margin,
    ROUND(SAFE_DIVIDE((SUM(total_revenue) - SUM(total_cost)), SUM(total_revenue)) * 100, 2) AS operating_margin_pct
FROM 
    CityFinancials
GROUP BY 
    `Destination`
ORDER BY 
    operating_margin_pct DESC;

-- ---------------------------------------------------------------------------------
-- QUERY 2: Cost Structure Breakdown by Client Segment
-- Purpose: Analyze how the logistical costs are distributed across the 1st Mile, 
-- Trunk (Bus Network), and Last Mile for Retail (B2B) vs. SME (B2C) clients.
-- ---------------------------------------------------------------------------------

SELECT 
    `Type of client`,
    SUM(`Total operational cost`) AS total_costs,
    -- Calculate percentage of total cost for each leg of the supply chain
    ROUND(SAFE_DIVIDE(SUM(`Cost first mile`), SUM(`Total operational cost`)) * 100, 2) AS pct_1st_mile,
    ROUND(SAFE_DIVIDE(SUM(`Cost linehaul`), SUM(`Total operational cost`)) * 100, 2) AS pct_trunk,
    ROUND(SAFE_DIVIDE(SUM(`Cost last mile`), SUM(`Total operational cost`)) * 100, 2) AS pct_last_mile
FROM 
    `project-edebec60-1723-4381-90f.dataset_kupos.datasetv3`
GROUP BY 
    `Type of client`;

-- ---------------------------------------------------------------------------------
-- QUERY 3: Identify Top 3 Pilot Routes using Window Functions
-- Purpose: Rank destination cities based on Net Margin to select the top 3 
-- most profitable routes for the initial strategic rollout.
-- ---------------------------------------------------------------------------------

WITH RouteMargins AS (
    SELECT 
        `Destination`,
        SUM(`Net margin`) AS net_margin
    FROM 
        `project-edebec60-1723-4381-90f.dataset_kupos.datasetv3`
    GROUP BY 
        `Destination`
),
RankedRoutes AS (
    SELECT 
        `Destination`,
        net_margin,
        RANK() OVER(ORDER BY net_margin DESC) as profitability_rank
    FROM 
        RouteMargins
)
SELECT 
    `Destination`,
    net_margin,
    profitability_rank
FROM 
    RankedRoutes
WHERE 
    profitability_rank <= 3;
