"""
Calibrate 23 Colleges & Career Tracks against the 500-case empirical profile dataset
"""

import json

# Calibrated college growth configurations to fit the 500-case empirical medians
TRACKS_CONFIG = [
    # Tier 1 Elite (IIM A/B/C)
    {"id": "iima", "name": "IIM Ahmedabad", "short": "IIM-A", "cluster": "Tier 1 Elite (IIM A/B/C)", "cluster_id": "c1", "color": "#10b981", "fee": 31.0, "loan": 30.0, "rate": 8.5, "dur": 2, "start_ctc": 34.5, "g1": 0.182, "g2": 0.132, "g3": 0.082},
    {"id": "iimb", "name": "IIM Bangalore", "short": "IIM-B", "cluster": "Tier 1 Elite (IIM A/B/C)", "cluster_id": "c1", "color": "#059669", "fee": 30.0, "loan": 30.0, "rate": 8.5, "dur": 2, "start_ctc": 34.0, "g1": 0.182, "g2": 0.132, "g3": 0.082},
    {"id": "iimc", "name": "IIM Calcutta", "short": "IIM-C", "cluster": "Tier 1 Elite (IIM A/B/C)", "cluster_id": "c1", "color": "#34d399", "fee": 31.0, "loan": 30.0, "rate": 8.5, "dur": 2, "start_ctc": 34.0, "g1": 0.182, "g2": 0.132, "g3": 0.082},
    
    # 1-Yr Fast Track (ISB)
    {"id": "isb", "name": "ISB Hyd / Mohali (1-Yr)", "short": "ISB", "cluster": "1-Yr Fast Track (ISB)", "cluster_id": "c2", "color": "#f59e0b", "fee": 42.0, "loan": 40.0, "rate": 8.5, "dur": 1, "start_ctc": 34.0, "g1": 0.178, "g2": 0.128, "g3": 0.082},
    
    # High ROI Kings (FMS, JBIMS, TISS)
    {"id": "fms", "name": "FMS Delhi", "short": "FMS", "cluster": "High ROI Kings", "cluster_id": "c3", "color": "#06b6d4", "fee": 2.0, "loan": 0.0, "rate": 8.5, "dur": 2, "start_ctc": 32.0, "g1": 0.178, "g2": 0.128, "g3": 0.080},
    {"id": "jbims", "name": "JBIMS Mumbai", "short": "JBIMS", "cluster": "High ROI Kings", "cluster_id": "c3", "color": "#0891b2", "fee": 6.0, "loan": 5.0, "rate": 8.5, "dur": 2, "start_ctc": 28.0, "g1": 0.175, "g2": 0.125, "g3": 0.080},
    {"id": "tiss", "name": "TISS Mumbai (HRM)", "short": "TISS", "cluster": "High ROI Kings", "cluster_id": "c3", "color": "#22d3ee", "fee": 2.5, "loan": 0.0, "rate": 8.5, "dur": 2, "start_ctc": 26.0, "g1": 0.172, "g2": 0.122, "g3": 0.078},
    
    # Tier 1 Premier (XLRI, SPJIMR, IIM L/K/M/I, SJMSOM)
    {"id": "spjimr", "name": "SPJIMR Mumbai", "short": "SPJIMR", "cluster": "Tier 1 Premier", "cluster_id": "c4", "color": "#818cf8", "fee": 24.0, "loan": 22.0, "rate": 8.5, "dur": 2, "start_ctc": 33.0, "g1": 0.175, "g2": 0.125, "g3": 0.080},
    {"id": "xlri", "name": "XLRI Jamshedpur", "short": "XLRI", "cluster": "Tier 1 Premier", "cluster_id": "c4", "color": "#6366f1", "fee": 30.0, "loan": 28.0, "rate": 8.5, "dur": 2, "start_ctc": 31.0, "g1": 0.175, "g2": 0.125, "g3": 0.080},
    {"id": "iiml", "name": "IIM Lucknow", "short": "IIM-L", "cluster": "Tier 1 Premier", "cluster_id": "c4", "color": "#4f46e5", "fee": 26.0, "loan": 25.0, "rate": 8.5, "dur": 2, "start_ctc": 30.0, "g1": 0.172, "g2": 0.122, "g3": 0.078},
    {"id": "iimk", "name": "IIM Kozhikode", "short": "IIM-K", "cluster": "Tier 1 Premier", "cluster_id": "c4", "color": "#a855f7", "fee": 23.0, "loan": 22.0, "rate": 8.5, "dur": 2, "start_ctc": 29.0, "g1": 0.170, "g2": 0.120, "g3": 0.078},
    {"id": "iimm", "name": "IIM Mumbai (NITIE)", "short": "IIM-M", "cluster": "Tier 1 Premier", "cluster_id": "c4", "color": "#c084fc", "fee": 21.0, "loan": 20.0, "rate": 8.5, "dur": 2, "start_ctc": 28.0, "g1": 0.168, "g2": 0.120, "g3": 0.076},
    {"id": "sjmsom", "name": "SJMSOM IIT Bombay", "short": "SJMSOM", "cluster": "Tier 1 Premier", "cluster_id": "c4", "color": "#9333ea", "fee": 14.0, "loan": 12.0, "rate": 8.5, "dur": 2, "start_ctc": 27.0, "g1": 0.168, "g2": 0.120, "g3": 0.076},
    {"id": "iimi", "name": "IIM Indore", "short": "IIM-I", "cluster": "Tier 1 Premier", "cluster_id": "c4", "color": "#7c3aed", "fee": 24.0, "loan": 22.0, "rate": 8.5, "dur": 2, "start_ctc": 26.5, "g1": 0.168, "g2": 0.120, "g3": 0.075},

    # Tier 1.5 & New IIMs (Gen 2: Trichy, Udaipur; MDI, IIFT, SIBM, NMIMS)
    {"id": "mdi", "name": "MDI Gurgaon", "short": "MDI", "cluster": "Tier 1.5 & New IIMs", "cluster_id": "c5", "color": "#f43f5e", "fee": 26.0, "loan": 24.0, "rate": 8.75, "dur": 2, "start_ctc": 26.0, "g1": 0.160, "g2": 0.115, "g3": 0.075},
    {"id": "iift", "name": "IIFT Delhi", "short": "IIFT", "cluster": "Tier 1.5 & New IIMs", "cluster_id": "c5", "color": "#fb7185", "fee": 23.0, "loan": 22.0, "rate": 8.75, "dur": 2, "start_ctc": 26.0, "g1": 0.160, "g2": 0.115, "g3": 0.075},
    {"id": "sibm", "name": "SIBM Pune", "short": "SIBM", "cluster": "Tier 1.5 & New IIMs", "cluster_id": "c5", "color": "#fda4af", "fee": 26.0, "loan": 24.0, "rate": 8.75, "dur": 2, "start_ctc": 24.0, "g1": 0.155, "g2": 0.112, "g3": 0.075},
    {"id": "nmims", "name": "NMIMS Mumbai", "short": "NMIMS", "cluster": "Tier 1.5 & New IIMs", "cluster_id": "c5", "color": "#e11d48", "fee": 26.0, "loan": 25.0, "rate": 9.0, "dur": 2, "start_ctc": 22.0, "g1": 0.150, "g2": 0.110, "g3": 0.072},
    {"id": "iimu", "name": "IIM Udaipur", "short": "IIM-U", "cluster": "Tier 1.5 & New IIMs", "cluster_id": "c5", "color": "#f87171", "fee": 22.0, "loan": 22.0, "rate": 8.75, "dur": 2, "start_ctc": 19.5, "g1": 0.162, "g2": 0.118, "g3": 0.076},
    {"id": "iimt", "name": "IIM Trichy", "short": "IIM-T", "cluster": "Tier 1.5 & New IIMs", "cluster_id": "c5", "color": "#ef4444", "fee": 21.0, "loan": 21.0, "rate": 8.75, "dur": 2, "start_ctc": 19.0, "g1": 0.162, "g2": 0.118, "g3": 0.076},

    # Undergrad Direct (No MBA)
    {"id": "srcc", "name": "SRCC Grad (Pure UG / No MBA)", "short": "SRCC (Pure UG)", "cluster": "Undergrad Direct (No MBA)", "cluster_id": "ug", "color": "#c084fc", "fee": 1.2, "loan": 0.0, "rate": 0.0, "dur": 0, "start_ctc": 12.0, "g1": 0.180, "g2": 0.118, "g3": 0.068, "ceiling_role": "Director / Principal (GCC / Tech Ops)", "ceiling_ctc": "₹65L - ₹85L (₹50L-₹65L fixed cash)", "ceiling_notes": "Starts in top capability hubs (BCN/D.E. Shaw); hits ceiling at Director level in GCCs without MBA/CA partner eligibility."},
    {"id": "venky", "name": "Venky / Deloitte UG (No MBA)", "short": "Deloitte / Venky", "cluster": "Undergrad Direct (No MBA)", "cluster_id": "ug", "color": "#eab308", "fee": 1.2, "loan": 0.0, "rate": 0.0, "dur": 0, "start_ctc": 6.0, "g1": 0.175, "g2": 0.132, "g3": 0.088, "ceiling_role": "Senior Manager / Associate Director", "ceiling_ctc": "₹40L - ₹58L (₹32L-₹45L fixed cash)", "ceiling_notes": "Partner track in Big 4 requires CA/CPA or Tier-1 MBA; transitions to Delivery Lead / Senior PMO managing onshore teams."},

    # Baby IIMs (Gen 3 Benchmark)
    {"id": "iim_amritsar", "name": "IIM Amritsar (Baby IIM MBA)", "short": "IIM Amritsar", "cluster": "Baby IIMs (Tier 2 Benchmark)", "cluster_id": "baby_iim", "color": "#f97316", "fee": 17.5, "loan": 16.0, "rate": 8.75, "dur": 2, "start_ctc": 15.5, "g1": 0.155, "g2": 0.115, "g3": 0.080, "ceiling_role": "Director / VP / Business Unit Head", "ceiling_ctc": "₹80L - ₹1.10 Cr (₹65L-₹85L fixed cash)", "ceiling_notes": "Lags SRCC in early years due to ₹17.5L debt; unconstrained by undergrad ceiling in later years to reach corporate Director/VP."}
]

def calc_new_regime_tax(income_lakhs):
    taxable = max(0.0, income_lakhs - 0.75)
    if taxable <= 7.0:
        return 0.0
    tax = 0.0
    tax += min(max(0.0, taxable - 3.0), 4.0) * 0.05
    if taxable > 7.0: tax += min(taxable - 7.0, 3.0) * 0.10
    if taxable > 10.0: tax += min(taxable - 10.0, 2.0) * 0.15
    if taxable > 12.0: tax += min(taxable - 12.0, 3.0) * 0.20
    if taxable > 15.0: tax += (taxable - 15.0) * 0.30
    surcharge = 0.0
    if taxable > 200.0: surcharge = tax * 0.25
    elif taxable > 100.0: surcharge = tax * 0.15
    elif taxable > 50.0: surcharge = tax * 0.10
    return (tax + surcharge) * 1.04

def compute_emi(loan_lakhs, rate_pct, tenure_years=7):
    if loan_lakhs <= 0: return 0, 0.0
    P = loan_lakhs * 100000.0
    r = (rate_pct / 100.0) / 12.0
    n = tenure_years * 12
    emi = P * r * ((1 + r)**n) / (((1 + r)**n) - 1)
    emi_mo = round(emi)
    emi_yr = (emi_mo * 12) / 100000.0
    return emi_mo, emi_yr

def simulate_track(cfg):
    dur = cfg["dur"]
    start_ctc = cfg["start_ctc"]
    g1, g2, g3 = cfg["g1"], cfg["g2"], cfg["g3"]
    emi_mo, emi_yr = compute_emi(cfg["loan"], cfg["rate"])
    
    gross_ctc = [0.0] * 20
    annual_in_hand = [0.0] * 20
    monthly_in_hand = [0.0] * 20
    cum_wealth = [0.0] * 20
    
    current_ctc = start_ctc
    work_years = 0
    total_wealth = 0.0
    
    for y in range(20):
        # Study years
        if dur == 2 and y < 2:
            gross_ctc[y] = 0.0
            annual_in_hand[y] = 0.0
            monthly_in_hand[y] = 0.0
            cum_wealth[y] = 0.0
            continue
        elif dur == 1 and y < 1:
            gross_ctc[y] = 0.0
            annual_in_hand[y] = 0.0
            monthly_in_hand[y] = 0.0
            cum_wealth[y] = 0.0
            continue
        
        # Working years
        if work_years == 0:
            current_ctc = start_ctc
        else:
            # Multi-phase S-curve growth
            if work_years <= 4:
                rate = g1
            elif work_years <= 10:
                rate = g2
            else:
                rate = g3
            current_ctc = current_ctc * (1 + rate)
        
        work_years += 1
        gross_ctc[y] = round(current_ctc, 2)
        
        # Real liquid cash factor (accounting for non-cash retiral, variable pool)
        cash_ratio = 0.88 if current_ctc < 40 else (0.82 if current_ctc < 100 else 0.78)
        taxable_cash = current_ctc * cash_ratio
        tax = calc_new_regime_tax(taxable_cash)
        post_tax_cash = taxable_cash - tax
        
        # Loan EMI active check (7 years)
        emi_active = False
        if dur == 2 and (2 <= y <= 8):
            emi_active = True
        elif dur == 1 and (1 <= y <= 7):
            emi_active = True
        
        net_in_hand = post_tax_cash - (emi_yr if emi_active else 0.0)
        net_in_hand = max(0.0, net_in_hand)
        
        annual_in_hand[y] = round(net_in_hand, 2)
        monthly_in_hand[y] = round(net_in_hand / 12.0, 2)
        
        # Progressive savings rate & 9% portfolio compounding
        savings_rate = 0.35 if current_ctc < 30 else (0.45 if current_ctc < 75 else 0.60)
        annual_saved = net_in_hand * savings_rate
        total_wealth = (total_wealth * 1.09) + annual_saved
        cum_wealth[y] = round(total_wealth / 100.0, 2)
        
    return {
        "id": cfg["id"],
        "name": cfg["name"],
        "short": cfg["short"],
        "cluster": cfg["cluster"],
        "cluster_id": cfg["cluster_id"],
        "color": cfg["color"],
        "fee": cfg["fee"],
        "loan": cfg["loan"],
        "rate": cfg["rate"],
        "dur": cfg["dur"],
        "emi_mo": emi_mo,
        "emi_yr": emi_yr,
        "start_ctc": cfg["start_ctc"],
        "annual_in_hand": annual_in_hand,
        "monthly_in_hand": monthly_in_hand,
        "gross_ctc": gross_ctc,
        "cum_wealth": cum_wealth,
        "total_wealth_20yr": cum_wealth[19],
        "y3_in_hand_mo": monthly_in_hand[2],
        "y10_in_hand_mo": monthly_in_hand[9],
        "y20_in_hand_mo": monthly_in_hand[19],
        "ceiling_role": cfg.get("ceiling_role", ""),
        "ceiling_ctc": cfg.get("ceiling_ctc", ""),
        "ceiling_notes": cfg.get("ceiling_notes", "")
    }

results = [simulate_track(c) for c in TRACKS_CONFIG]

if __name__ == "__main__":
    import os
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "data", "career_tracks_dataset.json")
    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved {len(results)} calibrated tracks to {dataset_path}")

    print(f"{'College':<15} | {'Fee':<5} | {'Y3 In-Hand':<10} | {'Y10 In-Hand':<11} | {'Y20 In-Hand':<11} | {'Y20 Gross':<10} | {'20Y Wealth':<10}")
    print("-" * 88)
    for r in results:
        print(f"{r['short']:<15} | {r['fee']:<5.1f} | ₹{r['y3_in_hand_mo']:<8.2f}L | ₹{r['y10_in_hand_mo']:<9.2f}L | ₹{r['y20_in_hand_mo']:<9.2f}L | ₹{r['gross_ctc'][19]:<8.1f}L | ₹{r['total_wealth_20yr']:<6.2f} Cr")

