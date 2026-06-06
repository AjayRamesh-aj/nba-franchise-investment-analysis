# NBA Franchise Investment Advisory
### A Moneyball-Style Strategy Consulting Framework

**Author:** Ajay Ramesh | Business Analytics  
**Tools:** Python, pandas, matplotlib, openpyxl  
**Data:** 30 NBA Franchises | 11 Seasons | 33,316 Game Records | 2013–2024

---

## Business Problem

NBA franchises spend hundreds of millions in player payroll every season — but higher spending does not guarantee wins. This project answers one question from an investor's perspective:

> **Which NBA franchises deliver the best return on payroll investment?**

---

## Analytical Framework

| Layer | Approach |
|-------|----------|
| KPI Development | Cost Per Win = Payroll / Total Wins |
| Segmentation | 4-Quadrant McKinsey-style Strategy Map |
| Risk Assessment | 3-Year Rolling Win % and Efficiency Trends |
| Investment Rating | BUY / HOLD / MONITOR / AVOID Framework |

---

## Key Findings

**1. Payroll does not buy championships**  
Golden State Warriors appear in both the top 5 most efficient franchises AND the top 5 worst investments — proving that talent development strategy matters more than spending.

**2. Small market teams deliver the best ROI**  
Oklahoma City Thunder achieved $1.65M cost per win in 2023-24 — the most efficient franchise in the dataset.

**3. Overspending on declining rosters destroys value**  
Washington Wizards spent $94M for only 15 wins in 2023-24 — $6.29M per win — the worst capital allocation in the league.

---

## Investment Recommendations (2023-24)

| Rating | Team | Cost Per Win | Rationale |
|--------|------|-------------|-----------|
| BUY | Oklahoma City Thunder | $1.65M | Rising asset, young core, best efficiency |
| BUY | Orlando Magic | $1.80M | Undervalued, improving trajectory |
| BUY | Indiana Pacers | $2.09M | Rising efficiency, strong upside |
| HOLD | Milwaukee Bucks | — | Cyclical performer, history of recovery |
| AVOID | Washington Wizards | $6.29M | Worst ROI, no rebuild strategy |
| AVOID | Detroit Pistons | $5.31M | 14 wins on high payroll |

---

## Deliverables

| File | Description |
|------|-------------|
| `analysis.py` | Full Python analysis pipeline — 10 sections |
| `NBA_Investment_Report.xlsx` | 4-sheet Excel report with formatted tables |
| `EXECUTIVE_BRIEF.md` | Boardroom memo in consulting format |
| `chart1_strategy_map.png` | 4-Quadrant Strategy Map |
| `chart2_top10_efficiency.png` | Top 10 Most Efficient Franchises |
| `chart3_win_trend.png` | Win % Trend Over Time |

---

*This project demonstrates business analytics, KPI development, strategic segmentation, investment risk assessment, and executive reporting — applied to a real-world dataset.*
