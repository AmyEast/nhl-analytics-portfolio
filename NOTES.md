# Project Notes & Future Analysis

## Future Projects / Hobby Repo
- **Penalty differential analysis** — do some teams get penalized more than 
  others? PIT specific interest. Uses play-by-play endpoint: 
  `/v1/gamecenter/{game_id}/play-by-play`
- **Betting odds integration** — The Odds API for historical odds (~$20/month). 
  Pull one month of historical data, then build live pipeline for next season. 
  Would upgrade H5 upset model significantly
- **Season-over-season comparison** — repeat analysis across multiple seasons 
  to validate findings
- **Full Corsi pull** — game-level shot data from individual game endpoints 
  for true possession metrics

## Phase 5 Enrichments
- **Team age analysis** — pull `birthDate` from roster endpoint for all 32 
  teams, correlate with H4 fatigue resilience score
- **Player games played** — via `/v1/player/{id}/landing` for context on 
  mid-season trades (e.g. Chinakhov)
- **Back-to-back type categorization** — home→away, away→home, away→away, 
  home→home using `location` field in `df_sched`
- **Expand H5 model** — add team quality, roster age, back-to-back type, 
  betting odds as features

## Methodological Notes
- **H5 NaN handling** — dropped ~20 rows with missing rest/travel data. 
  Alternative: impute with median. Loss is <2% of dataset so dropping is 
  defensible
- **H3 confounding variable** — West conference had fewer cumulative points 
  in 2025-26. Eastward/westward travel findings should be interpreted with 
  caution until controlled for team quality in expanded H5 model
- **Olympic break** — compressed schedule around break may inflate B2B rates 
  vs typical season

## Project Instructions
- Guide me to find answers myself, only provide code for genuinely new concepts