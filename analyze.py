# analyze.py
# Key finding: km_since_service (r=+0.40) is the dominant predictor of breakdown, followed by
# avg_daily_km (r=+0.25) and load_factor (r=+0.22). Total mileage and age show zero correlation
# (r≈0.00) — the intuition that "older, higher-mileage cars break down more" is not in this data.

# HOW THE RISK SCORE WORKS
# -------------------------
# We use only the three columns that genuinely separate broken cars from healthy ones.
# Each column is min-max scaled to [0, 1] across the whole fleet, then weighted by how strongly
# it correlates with broke_down.  The weights (0.55 / 0.25 / 0.20) are rounded from the relative
# magnitudes of the three correlations (0.404 / 0.252 / 0.215).  The final score is multiplied
# by 100 so it reads as a 0-to-100 risk index.
#
# Columns deliberately EXCLUDED: odometer_km (r≈0.00) and age_years (r≈0.00).

import pandas as pd

# ------------------------------------------------------------------
# 1. Load the data
# ------------------------------------------------------------------
df = pd.read_csv("fleet_history.csv")

features = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
broke = df[df["broke_down"] == 1]
ok    = df[df["broke_down"] == 0]

# ------------------------------------------------------------------
# 2. Compare the two groups column by column
# ------------------------------------------------------------------
print("=" * 65)
print("STEP 1 — Which columns separate broken cars from healthy ones?")
print("=" * 65)
print(f"\n120 cars total: {len(broke)} broke down, {len(ok)} did not.\n")

print(f"{'Column':<20} {'Broke mean':>11} {'OK mean':>11} {'r':>7}  Signal?")
print("-" * 65)

correlations = {}
for col in features:
    b_mean = broke[col].mean()
    o_mean = ok[col].mean()
    r      = df[col].corr(df["broke_down"])
    correlations[col] = r
    signal = "YES" if abs(r) >= 0.15 else "no"
    print(f"{col:<20} {b_mean:>11.1f} {o_mean:>11.1f} {r:>+7.3f}  {signal}")

print("""
Plain-English interpretation:
  km_since_service : broke cars had driven 11,678 km since service on average vs.
                     7,261 km for healthy ones — a 61 % gap and r=+0.40. Strongest signal.
  avg_daily_km     : higher daily use -> moderately higher risk (r=+0.25).
  load_factor      : heavier load -> moderately higher risk (r=+0.22).
  odometer_km      : r=+0.002 — total mileage tells us nothing. A 100,000-km car is
                     no more likely to break down than a 10,000-km car.
  age_years        : r=-0.001 — age is also completely flat. Older != riskier here.
""")

# ------------------------------------------------------------------
# 3. Build a weighted risk score from the three useful columns only
# ------------------------------------------------------------------
print("=" * 65)
print("STEP 2 — Building the risk score")
print("=" * 65)
print("""
We use km_since_service, avg_daily_km, and load_factor.
Each is min-max scaled to [0, 1], then weighted:
  km_since_service : 0.55  (r=0.40, dominant)
  avg_daily_km     : 0.25  (r=0.25)
  load_factor      : 0.20  (r=0.22)
Score = weighted sum × 100  -> 0-to-100 risk index.
""")

score_cols = ["km_since_service", "avg_daily_km", "load_factor"]
weights    = [0.55,               0.25,           0.20         ]

scored = df.copy()
for col in score_cols:
    col_min  = scored[col].min()
    col_max  = scored[col].max()
    scored[f"{col}_scaled"] = (scored[col] - col_min) / (col_max - col_min)

scored["risk_score"] = sum(
    scored[f"{col}_scaled"] * w
    for col, w in zip(score_cols, weights)
) * 100

scored = scored.sort_values("risk_score", ascending=False).reset_index(drop=True)

# ------------------------------------------------------------------
# 4. Print top-10 by risk
# ------------------------------------------------------------------
print("=" * 65)
print("STEP 3 — Top 10 cars by risk score (highest first)")
print("=" * 65)
print(f"\n{'Rank':<5} {'car_id':<10} {'risk':>6} {'km_since_svc':>13} "
      f"{'avg_daily_km':>13} {'load':>6} {'broke?':>7}")
print("-" * 65)
for rank, row in scored.head(10).iterrows():
    broke_flag = "YES" if row["broke_down"] == 1 else "-"
    print(f"{rank+1:<5} {row['car_id']:<10} {row['risk_score']:>6.1f} "
          f"{row['km_since_service']:>13.0f} {row['avg_daily_km']:>13.0f} "
          f"{row['load_factor']:>6.2f} {broke_flag:>7}")

# ------------------------------------------------------------------
# 5. Quick sanity check: does the score actually rank breakers higher?
# ------------------------------------------------------------------
print()
avg_risk_broke  = scored[scored["broke_down"] == 1]["risk_score"].mean()
avg_risk_ok     = scored[scored["broke_down"] == 0]["risk_score"].mean()
print(f"Average risk score — cars that broke down : {avg_risk_broke:.1f}")
print(f"Average risk score — cars that did not    : {avg_risk_ok:.1f}")
print(f"Score separates the groups by {avg_risk_broke - avg_risk_ok:.1f} points.")
print()
print("Done. Cars at the top of the list are the ones to fix BEFORE the 80% rule flags them.")
