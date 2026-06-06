# ============================================================
# NBA FRANCHISE INVESTMENT ANALYSIS
# Strategy Consulting Framework | Moneyball Approach
# Author: Ajay Ramesh
# ============================================================

# ── SECTION 1: IMPORTS ──────────────────────────────────────
import os
import pandas as pd

# ── SECTION 2: LOAD DATA ────────────────────────────────────
folder = "/Users/ajayramesh/Downloads/NBA-Data-2010-2024-main"

df      = pd.read_csv(os.path.join(folder, "regular_season_totals_2010_2024.csv"))
payroll = pd.read_csv(os.path.join(folder, "nba_payroll.csv"))

print("✅ Data loaded")

# ── SECTION 3: CLEAN DATA ───────────────────────────────────
df = df.drop(columns=["AVAILABLE_FLAG"])
df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
df["WIN"]       = df["WL"].apply(lambda x: 1 if x == "W" else 0)

print("✅ Data cleaned")

# ── SECTION 4: SEASON SUMMARY ───────────────────────────────
season_summary = df.groupby(["SEASON_YEAR", "TEAM_NAME"]).agg(
    GAMES_PLAYED   = ("WIN", "count"),
    TOTAL_WINS     = ("WIN", "sum"),
    AVG_PTS        = ("PTS", "mean"),
    AVG_REB        = ("REB", "mean"),
    AVG_AST        = ("AST", "mean"),
    AVG_PLUS_MINUS = ("PLUS_MINUS", "mean")
).reset_index()

season_summary["WIN_PCT"] = (
    season_summary["TOTAL_WINS"] / season_summary["GAMES_PLAYED"]
).round(3)

print("✅ Season summary built")

# ── SECTION 5: MERGE PAYROLL & BUSINESS METRICS ─────────────
merged = season_summary.merge(payroll, on=["SEASON_YEAR", "TEAM_NAME"], how="left")
merged = merged.dropna(subset=["PAYROLL_MILLIONS"])
merged["COST_PER_WIN"] = (merged["PAYROLL_MILLIONS"] / merged["TOTAL_WINS"]).round(2)

print("✅ Payroll merged")

# ── SECTION 6: 4-QUADRANT STRATEGY MAP ──────────────────────
median_wins = merged["TOTAL_WINS"].median()
median_cost = merged["COST_PER_WIN"].median()

def assign_quadrant(row):
    high_wins = row["TOTAL_WINS"] >= median_wins
    low_cost  = row["COST_PER_WIN"] <= median_cost
    if high_wins and low_cost:
        return "Star — High Wins, Low Cost"
    elif high_wins and not low_cost:
        return "Expensive Winner — High Wins, High Cost"
    elif not high_wins and low_cost:
        return "Undervalued — Low Wins, Low Cost"
    else:
        return "Poor Investment — Low Wins, High Cost"

merged["QUADRANT"] = merged.apply(assign_quadrant, axis=1)

print("✅ Quadrant analysis complete")
print("\n=== 4-QUADRANT BREAKDOWN ===")
print(merged["QUADRANT"].value_counts())
print(f"\nMedian Wins: {median_wins}")
print(f"Median Cost Per Win: ${median_cost}M")

print("\n--- TOP 5 STARS (Best ROI) ---")
stars = merged[merged["QUADRANT"] == "Star — High Wins, Low Cost"]
print(stars[["SEASON_YEAR","TEAM_NAME","TOTAL_WINS","PAYROLL_MILLIONS","COST_PER_WIN"]]
      .sort_values("COST_PER_WIN").head(5).to_string(index=False))

print("\n--- TOP 5 POOR INVESTMENTS (Worst ROI) ---")
poor = merged[merged["QUADRANT"] == "Poor Investment — Low Wins, High Cost"]
print(poor[["SEASON_YEAR","TEAM_NAME","TOTAL_WINS","PAYROLL_MILLIONS","COST_PER_WIN"]]
      .sort_values("COST_PER_WIN", ascending=False).head(5).to_string(index=False))
# ── SECTION 7: VISUALIZATIONS ───────────────────────────────
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── CHART 1: STRATEGY MAP SCATTER PLOT ──────────────────────

# Define a color for each quadrant
color_map = {
    "Star — High Wins, Low Cost"              : "#2ecc71",  # green
    "Expensive Winner — High Wins, High Cost" : "#3498db",  # blue
    "Undervalued — Low Wins, Low Cost"        : "#f39c12",  # orange
    "Poor Investment — Low Wins, High Cost"   : "#e74c3c",  # red
}

# Create the chart canvas
fig, ax = plt.subplots(figsize=(14, 9))

# Plot each quadrant as a separate group of dots
for quadrant, color in color_map.items():
    subset = merged[merged["QUADRANT"] == quadrant]
    ax.scatter(
        subset["PAYROLL_MILLIONS"],
        subset["TOTAL_WINS"],
        c=color,
        label=quadrant,
        alpha=0.7,
        s=80
    )

# Add dividing lines at the median
ax.axhline(y=median_wins, color="gray", linestyle="--", linewidth=1)
ax.axvline(x=merged["PAYROLL_MILLIONS"].median(), color="gray", linestyle="--", linewidth=1)

# Labels and title
ax.set_xlabel("Payroll ($ Millions)", fontsize=13)
ax.set_ylabel("Total Wins", fontsize=13)
ax.set_title("NBA Franchise Investment Strategy Map (2013–2024)\nPayroll vs Wins — Quadrant Analysis", fontsize=15, fontweight="bold")
ax.legend(loc="upper left", fontsize=10)

# Save the chart
output_path = os.path.join(folder, "chart1_strategy_map.png")
plt.tight_layout()
plt.savefig(output_path, dpi=150)
print(f"\n✅ Chart 1 saved: {output_path}")


# ── CHART 2: TOP 10 MOST EFFICIENT TEAMS ────────────────────
top10 = merged.nsmallest(10, "COST_PER_WIN").copy()
top10["LABEL"] = top10["TEAM_NAME"] + " (" + top10["SEASON_YEAR"] + ")"

fig, ax = plt.subplots(figsize=(14, 7))
bars = ax.barh(top10["LABEL"], top10["COST_PER_WIN"], color="#2ecc71", edgecolor="white")
for bar, val in zip(bars, top10["COST_PER_WIN"]):
    ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
            f"${val}M", va="center", fontsize=10)
ax.set_xlabel("Cost Per Win ($ Millions)", fontsize=12)
ax.set_title("Top 10 Most Efficient NBA Franchises by Cost Per Win (2013–2024)", fontsize=13, fontweight="bold")
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(folder, "chart2_top10_efficiency.png"), dpi=150)
plt.close()
print("✅ Chart 2 saved: chart2_top10_efficiency.png")

# ── CHART 3: WIN % TREND OVER TIME (TOP 5 TEAMS) ────────────
top_teams = (merged.groupby("TEAM_NAME")["TOTAL_WINS"]
             .mean()
             .nlargest(5)
             .index.tolist())

fig, ax = plt.subplots(figsize=(14, 7))
for team in top_teams:
    team_data = merged[merged["TEAM_NAME"] == team].sort_values("SEASON_YEAR")
    ax.plot(team_data["SEASON_YEAR"], team_data["WIN_PCT"],
            marker="o", label=team, linewidth=2)

ax.set_xlabel("Season", fontsize=12)
ax.set_ylabel("Win Percentage", fontsize=12)
ax.set_title("Win % Trend Over Time — Top 5 Franchises (2013–2024)", fontsize=13, fontweight="bold")
ax.legend(fontsize=10)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(folder, "chart3_win_trend.png"), dpi=150)
plt.close()
print("✅ Chart 3 saved: chart3_win_trend.png")
# ── SECTION 8: RISK ANALYSIS ────────────────────────────────

# Sort data so rolling calculations go in correct time order
merged = merged.sort_values(["TEAM_NAME", "SEASON_YEAR"]).reset_index(drop=True)

# Calculate 3-year rolling average win % and cost per win per team
merged["ROLLING_WIN_PCT"]    = (merged.groupby("TEAM_NAME")["WIN_PCT"]
                                .transform(lambda x: x.rolling(3, min_periods=1).mean())
                                .round(3))

merged["ROLLING_COST_PER_WIN"] = (merged.groupby("TEAM_NAME")["COST_PER_WIN"]
                                  .transform(lambda x: x.rolling(3, min_periods=1).mean())
                                  .round(2))

# Classify each team-season as Rising, Declining, Stable, or High-Risk
def classify_risk(row):
    if row["WIN_PCT"] >= 0.55 and row["COST_PER_WIN"] <= median_cost:
        return "Rising Asset"
    elif row["WIN_PCT"] >= 0.50 and row["COST_PER_WIN"] > median_cost:
        return "Stable Performer"
    elif row["WIN_PCT"] < 0.45 and row["COST_PER_WIN"] > median_cost:
        return "High-Risk Investment"
    else:
        return "Declining Asset"

merged["RISK_LABEL"] = merged.apply(classify_risk, axis=1)

print("✅ Risk analysis complete")
print("\n=== RISK CLASSIFICATION BREAKDOWN ===")
print(merged["RISK_LABEL"].value_counts())
# ── SECTION 9: INVESTMENT RATINGS ───────────────────────────

def assign_rating(row):
    if row["QUADRANT"] == "Star — High Wins, Low Cost" and row["RISK_LABEL"] == "Rising Asset":
        return "BUY"
    elif row["QUADRANT"] == "Star — High Wins, Low Cost":
        return "HOLD"
    elif row["QUADRANT"] == "Expensive Winner — High Wins, High Cost":
        return "HOLD"
    elif row["QUADRANT"] == "Undervalued — Low Wins, Low Cost" and row["RISK_LABEL"] == "Rising Asset":
        return "MONITOR"
    elif row["QUADRANT"] == "Poor Investment — Low Wins, High Cost" and row["RISK_LABEL"] == "High-Risk Investment":
        return "AVOID"
    else:
        return "MONITOR"

merged["INVESTMENT_RATING"] = merged.apply(assign_rating, axis=1)

print("✅ Investment ratings assigned")
print("\n=== INVESTMENT RATING BREAKDOWN ===")
print(merged["INVESTMENT_RATING"].value_counts())

print("\n--- BUY RATED TEAMS (Most Recent Season) ---")
buy_teams = merged[merged["INVESTMENT_RATING"] == "BUY"]
latest_buy = buy_teams[buy_teams["SEASON_YEAR"] == buy_teams["SEASON_YEAR"].max()]
print(latest_buy[["SEASON_YEAR","TEAM_NAME","TOTAL_WINS","COST_PER_WIN","RISK_LABEL"]]
      .sort_values("COST_PER_WIN").to_string(index=False))

print("\n--- AVOID RATED TEAMS (Most Recent Season) ---")
avoid_teams = merged[merged["INVESTMENT_RATING"] == "AVOID"]
latest_avoid = avoid_teams[avoid_teams["SEASON_YEAR"] == avoid_teams["SEASON_YEAR"].max()]
print(latest_avoid[["SEASON_YEAR","TEAM_NAME","TOTAL_WINS","COST_PER_WIN","RISK_LABEL"]]
      .sort_values("COST_PER_WIN", ascending=False).to_string(index=False))
# ── SECTION 10: EXCEL REPORT ─────────────────────────────────
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import openpyxl

output_excel = os.path.join(folder, "NBA_Investment_Report.xlsx")

with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:

    # ── SHEET 1: FULL DATA ───────────────────────────────────
    merged.to_excel(writer, sheet_name="Full Data", index=False)

    # ── SHEET 2: FRANCHISE RANKINGS ─────────────────────────
    rankings = merged.groupby("TEAM_NAME").agg(
        AVG_WINS         = ("TOTAL_WINS",    "mean"),
        AVG_WIN_PCT      = ("WIN_PCT",        "mean"),
        AVG_PAYROLL      = ("PAYROLL_MILLIONS","mean"),
        AVG_COST_PER_WIN = ("COST_PER_WIN",   "mean"),
    ).round(2).reset_index()
    rankings = rankings.sort_values("AVG_COST_PER_WIN")
    rankings.to_excel(writer, sheet_name="Franchise Rankings", index=False)

    # ── SHEET 3: INVESTMENT RECOMMENDATIONS ─────────────────
    latest = merged[merged["SEASON_YEAR"] == "2023-24"].copy()
    latest = latest[["TEAM_NAME","TOTAL_WINS","WIN_PCT","PAYROLL_MILLIONS",
                     "COST_PER_WIN","QUADRANT","RISK_LABEL","INVESTMENT_RATING"]]
    latest = latest.sort_values("INVESTMENT_RATING")
    latest.to_excel(writer, sheet_name="2023-24 Recommendations", index=False)

    # ── SHEET 4: TOP OPPORTUNITIES ───────────────────────────
    top_opps = merged[merged["INVESTMENT_RATING"] == "BUY"].sort_values("COST_PER_WIN")
    top_opps = top_opps[["SEASON_YEAR","TEAM_NAME","TOTAL_WINS","PAYROLL_MILLIONS",
                          "COST_PER_WIN","RISK_LABEL"]]
    top_opps.to_excel(writer, sheet_name="Top Opportunities", index=False)

# ── FORMAT THE EXCEL FILE ────────────────────────────────────
wb = openpyxl.load_workbook(output_excel)

header_fill  = PatternFill("solid", fgColor="1F4E79")
header_font  = Font(bold=True, color="FFFFFF", size=11)
center       = Alignment(horizontal="center", vertical="center")

rating_colors = {
    "BUY"    : "C6EFCE",
    "HOLD"   : "FFEB9C",
    "MONITOR": "DDEBF7",
    "AVOID"  : "FFC7CE",
}

for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]

    # Format headers
    for cell in ws[1]:
        cell.fill      = header_fill
        cell.font      = header_font
        cell.alignment = center

    # Auto-size columns
    for col in ws.columns:
        max_len = max((len(str(c.value)) for c in col if c.value), default=10)
        ws.column_dimensions[get_column_letter(col[0].column)].width = min(max_len + 4, 40)

    # Color investment ratings
    if sheet_name in ["2023-24 Recommendations", "Top Opportunities"]:
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                if cell.value in rating_colors:
                    cell.fill = PatternFill("solid", fgColor=rating_colors[cell.value])

wb.save(output_excel)
print(f"\n✅ Excel report saved: {output_excel}")