"""
Simulation of Multi-Phase S-Curve Career Compensation for Top Indian MBAs & UG Tracks
Accounts for:
1. Multi-phase decaying growth (Early velocity -> Mid consolidation -> Senior corporate plateau)
2. Indian New Tax Regime (FY 2024-25/2025-26 slabs, standard deduction, surcharges, cess)
3. 7-Year Education Loan EMIs
4. Generation 2 (New IIMs: Trichy/Udaipur) vs Generation 3 (Baby IIMs: Amritsar) differentiation
5. Realistic executive compensation bands benchmarked to Michael Page / Aon / Mercer India
6. Net cumulative wealth compounding with progressive savings rates
"""

import json

def calc_new_regime_tax(income_lakhs):
    """
    Computes tax under New Tax Regime (in Lakhs INR)
    Slabs:
    0 - 3L: 0%
    3 - 7L: 5%
    7 - 10L: 10%
    10 - 12L: 15%
    12 - 15L: 20%
    Above 15L: 30%
    Std deduction: 0.75L
    Surcharges:
    > 50L: 10%
    > 100L: 15%
    > 200L: 25%
    Cess: 4%
    """
    taxable = max(0.0, income_lakhs - 0.75)
    if taxable <= 3.0:
        return 0.0
    
    # Rebate up to 7L taxable (Section 87A)
    if taxable <= 7.0:
        return 0.0

    tax = 0.0
    # 3 to 7: 4L @ 5% = 0.20L
    tax += min(max(0.0, taxable - 3.0), 4.0) * 0.05
    # 7 to 10: 3L @ 10% = 0.30L
    if taxable > 7.0:
        tax += min(taxable - 7.0, 3.0) * 0.10
    # 10 to 12: 2L @ 15% = 0.30L
    if taxable > 10.0:
        tax += min(taxable - 10.0, 2.0) * 0.15
    # 12 to 15: 3L @ 20% = 0.60L
    if taxable > 12.0:
        tax += min(taxable - 12.0, 3.0) * 0.20
    # Above 15L: 30%
    if taxable > 15.0:
        tax += (taxable - 15.0) * 0.30

    # Surcharge
    surcharge = 0.0
    if taxable > 200.0:
        surcharge = tax * 0.25
    elif taxable > 100.0:
        surcharge = tax * 0.15
    elif taxable > 50.0:
        surcharge = tax * 0.10

    total_tax = (tax + surcharge) * 1.04
    return total_tax

def compute_emi(loan_lakhs, rate_pct, tenure_years=7):
    if loan_lakhs <= 0:
        return 0.0, 0.0
    P = loan_lakhs * 100000.0
    r = (rate_pct / 100.0) / 12.0
    n = tenure_years * 12
    emi = P * r * ((1 + r)**n) / (((1 + r)**n) - 1)
    emi_mo = round(emi)
    emi_yr = (emi_mo * 12) / 100000.0 # in Lakhs
    return emi_mo, emi_yr

print("Tax on 34.5L:", calc_new_regime_tax(34.5))
print("Tax on 100L:", calc_new_regime_tax(100.0))
print("Tax on 200L:", calc_new_regime_tax(200.0))
