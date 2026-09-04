# Career Tracker: 20-Year Compensation & Wealth Simulation Engine
import json
import numpy as np
import matplotlib.pyplot as plt

def calc_tax(gross):
    """Calculates income tax under Indian New Tax Regime (Budget 2024-2026) + Surcharges + Cess."""
    if gross <= 0: return 0.0
    taxable = max(0, gross - 0.75) # Standard deduction of ₹75,000
    if taxable <= 7.0: return 0.0
    tax = 0.0
    if taxable > 3.0: tax += min(taxable - 3.0, 4.0) * 0.05
    if taxable > 7.0: tax += min(taxable - 7.0, 3.0) * 0.10
    if taxable > 10.0: tax += min(taxable - 10.0, 2.0) * 0.15
    if taxable > 12.0: tax += min(taxable - 12.0, 3.0) * 0.20
    if taxable > 15.0: tax += (taxable - 15.0) * 0.30
    surcharge_rate = 0.0
    if taxable > 200.0: surcharge_rate = 0.25
    elif taxable > 100.0: surcharge_rate = 0.15
    elif taxable > 50.0: surcharge_rate = 0.10
    return round(tax * (1 + surcharge_rate) * 1.04, 2)

def calculate_emi(principal_lakhs, annual_rate, tenure_months=84):
    """Calculates monthly loan EMI post-moratorium (in ₹)."""
    if principal_lakhs <= 0: return 0
    P = principal_lakhs * 100000
    r = (annual_rate / 100) / 12
    n = tenure_months
    return round((P * r * ((1 + r)**n)) / (((1 + r)**n - 1)))

if __name__ == "__main__":
    with open("../data/career_tracks_dataset.json") as f:
        tracks = json.load(f)
    print(f"Loaded {len(tracks)} career tracks successfully.")
