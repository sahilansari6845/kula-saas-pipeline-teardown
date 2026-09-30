# Kula.ai Pipeline & Revenue Leakage Analysis

An exploratory B2B SaaS funnel teardown modeling mid-market lead velocity, demo show rates, and product adoption thresholds.

## Key Insights Discovered
- **Top-Funnel Calendar Leak:** Cold Outbound leads show a **43.6% demo no-show rate** (56.4% attendance) compared to 84.0% for Referral channels.
- **The Activation Threshold:** Prospects conducting $\ge$50 candidate outreach sequences during the pilot stage convert at **66.7%**, compared to **19.7%** for sub-50 sequence volume (a 3.4x conversion lift).
- **Revenue Impact:** Outbound accounts generated $786k ARR compared to $1.3M+ from referrals, driven primarily by mid-funnel conversion leakage.

## Tech Stack & Deliverables
- **Data Modeling & Analytics:** Python, Pandas, NumPy
- **Interactive UI:** Streamlit, Plotly
- **Live Local Dashboard:** Run via `streamlit run app.py`

## Actionable Recommendations
1. **Reduce Demo No-Shows:** Introduce automated WhatsApp/SMS calendar reminders and a 1-click reschedule link for outbound prospects.
2. **Drive Trial Adoption:** Product onboarding should incentivize sending the first 50 outreach sequences within Day 3 of trial to trigger the activation threshold.
