import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pickle

# Page config
st.set_page_config(
    page_title="NHL Analytics Dashboard",
    page_icon="🏒",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    conn = sqlite3.connect('database/nhl.db')
    df_standings = pd.read_sql_query("SELECT * FROM standings", conn)
    df_schedule = pd.read_sql_query("SELECT * FROM schedule_with_rest", conn)
    df_players = pd.read_sql_query("SELECT * FROM players", conn)
    conn.close()

    with open('models/model_balanced.pkl', 'rb') as f:
        model = pickle.load(f)

    return df_standings, df_schedule, df_players, model

df_standings, df_schedule, df_players, model = load_data()

# Sidebar
st.sidebar.title("🏒 NHL Analytics")
st.sidebar.markdown("2025-26 Season Analysis")

page = st.sidebar.radio(
    "Navigate to:",
    ["Standings Overview", "Team Fatigue Profile", "Game Fatigue Explorer"]
)

if page == "Standings Overview":
    st.title("NHL Standings & Team Profiles")
    st.markdown("Explore how teams performed across offense, defense, and overall standing.")
    
    df_standings['goals_for_pg'] = (df_standings['goalFor'] / df_standings['gamesPlayed']).round(2)
    df_standings['goals_against_pg'] = (df_standings['goalAgainst'] / df_standings['gamesPlayed']).round(2)
    
    fig = px.scatter(
        df_standings,
        x='goals_for_pg',
        y='goals_against_pg',
        text='team_abbrev',
        color='conferenceName',
        size='points',
        hover_data=['team_name', 'points', 'wins', 'losses'],
        title='NHL Teams: Offense vs Defense Profile (2025-26)',
        labels={
            'goals_for_pg': 'Goals For Per Game (Offense)',
            'goals_against_pg': 'Goals Against Per Game (Defense)'
        }
    )
    fig.update_yaxes(autorange='reversed')
    fig.update_traces(textposition='top center')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Team Fatigue Profile":
    st.title("Team Fatigue Profile")
    st.markdown("Select a team to see how back-to-back games affect their performance.")
    
    # Team selector
    teams = sorted(df_schedule['away_team'].unique())
    selected_team = st.selectbox("Select a team", teams)
    
    # Filter schedule for selected team
    team_away = df_schedule[df_schedule['away_team'] == selected_team]
    team_home = df_schedule[df_schedule['home_team'] == selected_team]
    
    # Calculate overall win rate
    away_wins = (team_away['winner'] == selected_team).sum()
    home_wins = (team_home['winner'] == selected_team).sum()
    total_games = len(team_away) + len(team_home)
    overall_win_rate = (away_wins + home_wins) / total_games

    # Calculate B2B win rate
    b2b_away = team_away[team_away['away_rest'] == 0]
    b2b_home = team_home[team_home['home_rest'] == 0]
    b2b_wins = (b2b_away['winner'] == selected_team).sum() + (b2b_home['winner'] == selected_team).sum()
    b2b_games = len(b2b_away) + len(b2b_home)
    b2b_win_rate = b2b_wins / b2b_games if b2b_games > 0 else 0

    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Win Rate", f"{overall_win_rate:.1%}")
    col2.metric("B2B Win Rate", f"{b2b_win_rate:.1%}")
    col3.metric("Fatigue Impact", f"{(b2b_win_rate - overall_win_rate):.1%}", 
                delta_color="inverse")
    st.caption("Fatigue Impact = B2B Win Rate minus Overall Win Rate. Negative values indicate the team performs worse on back-to-back games. Note: games with missing rest data (season opener, post-Olympic break) are excluded from B2B counts.")
    
    # B2B type breakdown
    st.subheader("Back-to-Back Type Breakdown")
    
    b2b_types = {
        'away→away': (b2b_away[b2b_away['away_b2b_type'] == 'away→away']['winner'] == selected_team).mean(),
        'home→away': (b2b_away[b2b_away['away_b2b_type'] == 'home→away']['winner'] == selected_team).mean(),
        'away→home': (b2b_home[b2b_home['home_b2b_type'] == 'away→home']['winner'] == selected_team).mean(),
        'home→home': (b2b_home[b2b_home['home_b2b_type'] == 'home→home']['winner'] == selected_team).mean(),
    }

    b2b_counts = {
        'away→away': len(b2b_away[b2b_away['away_b2b_type'] == 'away→away']),
        'home→away': len(b2b_away[b2b_away['away_b2b_type'] == 'home→away']),
        'away→home': len(b2b_home[b2b_home['home_b2b_type'] == 'away→home']),
        'home→home': len(b2b_home[b2b_home['home_b2b_type'] == 'home→home']),
    }
    
    df_b2b = pd.DataFrame({
        'B2B Type': list(b2b_types.keys()),
        'Win Rate': list(b2b_types.values()),
        'Games': list(b2b_counts.values())
    })

    fig = px.bar(df_b2b, x='B2B Type', y='Win Rate',
             hover_data=['Games'],
             title=f'{selected_team} Win Rate by B2B Type',
             color='Win Rate', color_continuous_scale='RdYlGn')
    
    fig.add_hline(y=overall_win_rate, line_dash='dash', 
                  annotation_text='Overall Win Rate')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Game Fatigue Explorer":
    st.title("Game Fatigue Explorer")
    st.markdown("Select two teams to explore rest differential and estimate upset probability.")
    
    teams = sorted(df_schedule['away_team'].unique())
    
    col1, col2 = st.columns(2)
    with col1:
        away_team = st.selectbox("Away Team", teams, index=teams.index('PIT'))
    with col2:
        home_team = st.selectbox("Home Team", teams, index=teams.index('BUF'))
    
    away_rest = st.slider("Away Team Rest Days", 0, 7, 1)
    home_rest = st.slider("Home Team Rest Days", 0, 7, 1)
    tz_shift = st.slider("Timezone Shift (hours)", -3, 3, 0)
    
    rest_diff = away_rest - home_rest
    
    st.subheader("Rest Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Away Rest Days", away_rest)
    col2.metric("Home Rest Days", home_rest)
    col3.metric("Rest Differential", rest_diff)
    
    # Historical matchup rest stats
    st.subheader("Historical Context")
    matchups = df_schedule[
        (df_schedule['away_team'] == away_team) & 
        (df_schedule['home_team'] == home_team)
    ]
    
    if len(matchups) > 0:
        st.write(f"{away_team} vs {home_team} this season: {len(matchups)} games")
        away_wins = (matchups['winner'] == away_team).sum()
        st.write(f"{away_team} won {away_wins} of {len(matchups)} matchups")
    else:
        st.write("No direct matchups found this season.")
    
    # Upset probability prediction
    st.subheader("Upset Probability Estimate")
    
    # Get team win percentages from standings
    away_winpctg = df_standings[df_standings['team_abbrev'] == away_team]['winPctg'].values
    away_rolling = df_schedule[df_schedule['away_team'] == away_team]['away_rolling_win_rate'].dropna().iloc[-1] if len(df_schedule[df_schedule['away_team'] == away_team]) > 0 else 0.5
    
    if len(away_winpctg) > 0:
        away_winpctg = away_winpctg[0]
        
        # Build feature vector
        import numpy as np
        features = np.array([[rest_diff, tz_shift, away_rest, home_rest, 
                             away_winpctg, away_rolling]])
        
        # Load model and predict
        upset_prob = model.predict_proba(features)[0][1]
        
        st.metric("Estimated Upset Probability", f"{upset_prob:.1%}")
        with st.expander("See model inputs"):
            home_winpctg = df_standings[df_standings['team_abbrev'] == home_team]['winPctg'].values
            home_winpctg = home_winpctg[0] if len(home_winpctg) > 0 else 0.5
            
            st.write(f"**Away team season win %:** {away_winpctg:.1%}")
            st.write(f"**Away team current form (rolling win rate):** {away_rolling:.1%}")
            st.write(f"**Home team season win %:** {home_winpctg:.1%}")
            st.write(f"**Rest differential:** {rest_diff} days (positive favors away team)")
            st.write(f"**Timezone shift:** {tz_shift} hours")
            st.write(f"**Is away team the weaker team?** {'Yes — upset scenario' if away_winpctg < home_winpctg else 'No — away team is stronger'}")
        st.caption("Upset defined as the weaker away team winning. Probability based on rest, travel, and team quality variables.")
    else:
        st.write("Team data not available.")