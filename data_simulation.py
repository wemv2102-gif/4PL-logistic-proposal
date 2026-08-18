"""
=============================================================================
FILE: data_simulation.py
PROJECT: 4PL Logistics Optimization - Idle Capacity Monetization
AUTHOR: Williams Moreno

DESCRIPTION:
This script generates a synthetic dataset simulating daily parcel shipments 
for a 4PL logistics model. It incorporates real-world Chilean logistics 
benchmarks (e.g., Starken base fees), geographical distribution across 
Santiago communes and regional hubs, and seasonal volume peaks 
(CyberDay, CyberMonday, Christmas).
=============================================================================
"""

import datetime
import numpy as np
import pandas as pd

# Set seed for reproducibility
np.random.seed(42)
n_rows = 7500

# 1. Business Parameters Definition
client_types = ['Pyme', 'Retail']
prob_client = [0.6, 0.4]  # 60% SME (Pyme), 40% Retail

# Dispersed SME pickup origins in Santiago
sme_origin_communes = [
    'Santiago',
    'Providencia',
    'Las Condes',
    'Maipú',
    'La Florida',
    'San Miguel',
    'Ñuñoa',
]

# Consolidated B2B Retail hubs
retail_hubs = ['Pudahuel', 'Quilicura', 'San Bernardo']

destinations = [
    'Rancagua',
    'Valparaíso',
    'La Serena',
    'Concepción',
    'Temuco',
    'Puerto Montt',
    'Antofagasta',
]

# 2. Real Benchmark Rates (Starken Base Fee by Destination)
sme_base_fee = {
    'Rancagua': 3600,
    'Valparaíso': 4400,
    'La Serena': 4800,
    'Concepción': 4800,
    'Temuco': 5200,
    'Puerto Montt': 5800,
    'Antofagasta': 8200,
}

# Approximate linehaul cost per m3 based on distance
linehaul_cost_m3 = {
    'Rancagua': 1200,
    'Valparaíso': 1500,
    'La Serena': 2200,
    'Concepción': 2500,
    'Temuco': 3000,
    'Puerto Montt': 3800,
    'Antofagasta': 5500,
}

# 3. Seasonality Date Generation (CyberDay, CyberMonday, Christmas peaks)
months = list(range(1, 13))
month_weights = [
    0.06, 0.05, 0.07, 0.07, 0.15, 0.06,
    0.06, 0.07, 0.07, 0.14, 0.08, 0.12,
]
month_weights = np.array(month_weights) / sum(month_weights)

generated_months = np.random.choice(months, size=n_rows, p=month_weights)
dates = []
for m in generated_months:
    max_days = 30 if m in [4, 6, 9, 11] else (28 if m == 2 else 31)
    d = np.random.randint(1, max_days + 1)
    dates.append(f'2025-{m:02d}-{d:02d}')

# 4. Full Dataset Generation
data = []

for i in range(n_rows):
    client = np.random.choice(client_types, p=prob_client)
    date = dates[i]
    destination = np.random.choice(destinations)

    if client == 'Pyme':
        origin = np.random.choice(sme_origin_communes)
        volume_m3 = round(np.random.uniform(0.01, 0.15), 3)  # Individual parcels

        # Fee adjusted to real regional benchmark
        base_f = sme_base_fee[destination]
        fee = int(base_f * np.random.uniform(0.95, 1.25))

        # SME First Mile (Dispersed collection via independent drivers)
        cost_1st_mile = int(np.random.uniform(1600, 2100))
        cost_last_mile = int(np.random.uniform(1200, 1600))

        # Linehaul cost based on distance
        base_lh = linehaul_cost_m3[destination]
        linehaul_cost = int(600 + (volume_m3 * base_lh * 2))

    else:  # Retail (Consolidated B2B in Hubs)
        origin = np.random.choice(retail_hubs)
        volume_m3 = round(np.random.uniform(0.3, 1.8), 3)  # Pallets / Wholesale load

        # Retail negotiated B2B tariff based on volume
        base_f = sme_base_fee[destination]
        fee = int((base_f * 0.75) + (volume_m3 * 3500))

        # Retail First Mile (Consolidated from Hub)
        cost_1st_mile = int(np.random.uniform(500, 900))
        cost_last_mile = int(np.random.uniform(900, 1300))

        # Linehaul cost for full truck / massive overflow
        base_lh = linehaul_cost_m3[destination]
        linehaul_cost = int(800 + (volume_m3 * base_lh * 0.6))

    total_op_cost = cost_1st_mile + cost_last_mile + linehaul_cost
    net_margin = fee - total_op_cost

    data.append({
        'id_envio': f'KUP-{10000 + i}',
        'fecha_envio': date,
        'Type of client': client,
        'Origin': origin,
        'Destination': destination,
        'Volume m3': volume_m3,
        'Fee': fee,
        'Cost first mile': cost_1st_mile,
        'Cost last mile': cost_last_mile,
        'Cost linehaul': linehaul_cost,
        'Total operational cost': total_op_cost,
        'Net margin': net_margin,
    })

# 5. DataFrame Creation and Export
df_final = pd.DataFrame(data)
df_final.to_csv('kargo_simulation_dataset.csv', index=False)

print('✅ Dataset kargo_simulation_dataset.csv generated successfully!')
