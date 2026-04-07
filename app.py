import streamlit as st
import pandas as pd
from pathlib import Path
import os
import sys

# Ensure src in path
sys.path.append(os.path.dirname(__file__))

st.set_page_config(
    page_title="Frauen Bundesliga Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

st.title("Frauen Bundesliga Advanced Analytics")
st.caption("Made by **Afiq Akmal**")
st.markdown("""
Welcome to the Frauen Bundesliga Analytics Engine! 

This modern analytics portal utilizes high-end machine learning algorithms (XGBoost) combined with SHAP Value theory to decode exactly what it takes to:
1. **Win the League**
2. **Qualify for Top 25%**
3. **Survive Relegation**

Use the sidebar to navigate to:
- **League Insights**: Discover the overarching blueprint for success and the most vital team playstyle metrics.
- **Team Recommender**: Choose an objective and a specific team from the 25_26 season to get tailored actionable recommendations on fixing team metrics.
""")

st.info("Ensure to check both playstyle metrics and structural differences across seasons.")

# Add some custom CSS
st.markdown("""
<style>
    /* Add gradient header */
    h1 {
        background: -webkit-linear-gradient(45deg, #1E88E5, #D32F2F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# Central Data Cache Loader
@st.cache_data
def load_all_data(version=5): # Incremented version
    from src.pipeline import load_team_standings, load_all_team_stats
    from src.player_pipeline import load_and_score_players, get_squad_profiles
    
    standings = load_team_standings()
    team_stats = load_all_team_stats()
    
    # Load and process player profiles
    players_df = load_and_score_players()
    squad_profiles = get_squad_profiles(players_df)
    
    # Merge team stats with standings
    merged = pd.merge(team_stats, standings, on=['Team', 'Season'], how='inner')
    
    # Merge with squad profiles
    if not squad_profiles.empty:
        # Note: Player Stats only available for 24_25 and 25_26
        merged = pd.merge(merged, squad_profiles, on=['Team', 'Season'], how='left').fillna(0)
        
    return merged, team_stats, standings, players_df

with st.spinner("Loading Data and Models..."):
    merged_data, team_stats, standings, raw_players = load_all_data(version=5)
    st.session_state['merged_data'] = merged_data
    st.session_state['raw_players'] = raw_players

st.success("Data Pipeline Engine Initialized successfully.")

st.markdown("### Preview Teams Loaded")
st.dataframe(merged_data[['Season', 'Team', 'Rank', 'Points', 'Expected points']].head())
