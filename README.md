# NHL Analytics Portfolio

Exploratory and predictive analysis of NHL data examining team performance, 
player production, and the impact of schedule fatigue on game outcomes.

## The Question

Does schedule fatigue — back-to-back games, rest differentials, and 
cross-timezone travel — meaningfully shape NHL game outcomes? And can 
we predict the probability of an upset from fatigue variables alone?

## Key Findings

The NHL API had an incredibly (and surprisingly) rich dataset that enabled 
this analysis. From my analysis I can see that fatigue and timezone travel 
do affect performance, especially with large timezone differences which had 
the most impact in the logistic regression, but there are still many other 
variables that affect performance and the outcome of games. The full picture 
of how fatigue affects outcomes remains complex and warrants further analysis.

One interesting finding was that teams that generally finished outside 
playoff contention — such as the Kraken, Devils, Toronto, and Sharks — had 
some of the largest positive fatigue impact (B2B win rate minus overall win 
rate) versus teams like Colorado, who won the President's Trophy, who had a 
negative fatigue impact. Part of this could be sample size, bad luck, or 
injuries, but one thing to note is that many of these teams are on the coast 
and could be the beneficiaries of the largest timezone differential for 
visiting teams. The further into the project I went the more I realized 
there were several other variables that could be affecting outcomes given 
the reality of the 2025-26 season and team dynamics within it.

## Hypotheses Tested (Phase 4: The Hidden Opponent)

| Hypothesis | Finding |
|------------|---------|
| H1: Teams on back-to-backs win less often | ✅ Confirmed — away teams on B2Bs win 42% vs 47.8% overall |
| H2: Rest differential predicts outcomes | ✅ Confirmed — equal rest nearly eliminates home ice advantage (50.2%) |
| H3: Cross-timezone travel compounds fatigue | ⚠️ Partially supported — large shifts show effect but confounding variables exist |
| H4: Some teams are more resilient to fatigue | ✅ Confirmed — significant variance across all 32 teams |
| H5: Logistic regression can predict upset probability | ⚠️ Limited — rest/travel variables alone insufficient for reliable upset prediction; timezone shift emerged as strongest single predictor |

## Notebooks

| Notebook | Description |
|----------|-------------|
| `01_data_pipeline.ipynb` | NHL API connection and standings data pipeline |
| `02_team_analysis.ipynb` | Standings overview, offense/defense splits, home/road performance, possession proxy |
| `03_player_analysis.ipynb` | Points leaders, scorer vs playmaker analysis, Pittsburgh Penguins deep dive |
| `04_schedule_fatigue.ipynb` | Schedule fatigue analysis — rest days, timezone travel, team resilience, logistic regression model |

## In Progress / Upcoming Enhancements

- **H5 Model Enhancement** — adding team quality variables (points percentage) 
  alongside rest and travel for a more robust upset prediction model
- **Back-to-Back Type Analysis** — categorizing B2B games by travel pattern 
  (home→away, away→home, etc.) to isolate travel fatigue from rest fatigue
- **Rolling Win Rate** — replacing season-wide win percentage with rolling 
  win rate at time of game for more accurate team quality measurement

## Tech Stack

- **Python** — pandas, matplotlib, seaborn, plotly, scikit-learn
- **SQLite** — local database layer for structured querying across notebooks
- **Jupyter Notebooks** — analysis and narrative
- **NHL API** — `api-web.nhle.com` (no authentication required)

## Setup

```bash
git clone https://github.com/AmyEast/nhl-analytics-portfolio.git
cd nhl-analytics-portfolio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then open any notebook in Jupyter or VS Code/Cursor and run all cells.

## Project Status

🟡 In progress — Phase 5 polish and Streamlit dashboard in development

## Author

Amy East — [GitHub](https://github.com/AmyEast)