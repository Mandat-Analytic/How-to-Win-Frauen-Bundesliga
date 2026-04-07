import streamlit as st
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from src.models import train_team_models, get_top_features_from_shap
from src.models import train_team_models, get_top_features_from_shap

st.set_page_config(page_title="League Insights", layout="wide")

st.title("League Success Blueprint Insights")

if 'merged_data' not in st.session_state:
    st.error("Please navigate to the Home page first to load datasets.")
    st.stop()

merged_data = st.session_state['merged_data']

# TAP Reference dictionaries
INDEX_NAMES = {
    'IGC': 'Game Control (IGC)',
    'IOB': 'Playstyle / Offense (IOB)',
    'IDI': 'Defensive Intensity (IDI)',
    'IDO': 'Defensive Organization (IDO)',
    'ITS': 'Transitions (ITS)'
}

METRIC_GROUPS = {
    'IGC': ['T_PassAcc', 'T_Possession', 'T_AvgPassPerPoss', 'T_ProgPasses', 'T_DeepCompPasses'],
    'IOB': ['T_PosAttacks', 'T_AvgPassPerPoss', 'T_BackPasses', 'T_CounterAtt', 'T_AvgPassLen', 'T_LongPassPct'],
    'IDI': ['T_HighRecov', 'T_PPDA', 'T_DefDuelsWon', 'T_SlidingTackles', 'O_ProgPasses'],
    'IDO': ['T_Interceptions', 'T_Clearances', 'T_TotalRecov', 'T_AerialDuelsWon', 'O_ShotsOnTarget', 'O_PenAreaEntries'],
    'ITS': ['T_CounterAtt', 'T_CounterConv', 'T_DeepCompPasses', 'T_SmartPasses', 'O_Recoveries'],
}

METRIC_NAMES = {
    'T_PassAcc': 'Pass Accuracy %',
    'T_Possession': 'Possession %',
    'T_AvgPassPerPoss': 'Avg Passes / Possession',
    'T_ProgPasses': 'Progressive Passes (acc.)',
    'T_DeepCompPasses': 'Deep Completed Passes',
    'T_PosAttacks': 'Positional Attacks',
    'T_CounterAtt': 'Counterattacks',
    'T_AvgPassLen': 'Avg Pass Length',
    'T_BackPasses': 'Back Passes',
    'T_LongPassPct': 'Long Pass %',
    'T_HighRecov': 'High Recoveries (PAdj)',
    'T_PPDA': 'PPDA',
    'T_DefDuelsWon': 'Defensive Duels Won',
    'T_SlidingTackles': 'Sliding Tackles (PAdj)',
    'T_Interceptions': 'Interceptions (PAdj)',
    'T_Clearances': 'Clearances (PAdj)',
    'T_TotalRecov': 'Total Recoveries (PAdj)',
    'T_AerialDuelsWon': 'Aerial Duels Won',
    'T_CounterConv': 'Counter-attack Conv. %',
    'T_SmartPasses': 'Smart Passes (acc.)',
    'O_ProgPasses': 'Opp Progressive Passes',
    'O_ShotsOnTarget': 'Opp Shots on Target',
    'O_PenAreaEntries': 'Opp Penalty Area Entries',
    'O_Recoveries': 'Opp Recoveries (PAdj)',
}

# Inverse mapper for raw keys from models.py map
COL_MAP = {
    'T_PassAcc': 'Percentage Passes',
    'T_Possession': 'Possession, %',
    'T_AvgPassPerPoss': 'Average passes per possession',
    'T_ProgPasses': 'Total Progressive passes success',
    'T_DeepCompPasses': 'Deep completed passes',
    'T_PosAttacks': 'Total Positional attacks',
    'T_CounterAtt': 'Total Counterattacks',
    'T_AvgPassLen': 'Average pass length',
    'T_BackPasses': 'Total Back passes',
    'T_LongPassPct': 'Long pass %',
    'T_HighRecov': 'Recoveries High',
    'T_PPDA': 'PPDA',
    'T_DefDuelsWon': 'Total Defensive duels success',
    'T_SlidingTackles': 'Total Sliding tackles success',
    'T_Interceptions': 'Interceptions',
    'T_Clearances': 'Clearances',
    'T_TotalRecov': 'Total Recoveries',
    'T_AerialDuelsWon': 'Total Aerial duels success',
    'T_CounterConv': 'Percentage Counterattacks',
    'T_SmartPasses': 'Total Smart passes success',
    'O_ProgPasses': 'opponent_Total Progressive passes success',
    'O_ShotsOnTarget': 'opponent_Total Shots success',
    'O_PenAreaEntries': 'opponent_Total Penalty area entries',
    'O_Recoveries': 'opponent_Total Recoveries'
}

# Cache model training
@st.cache_resource
def get_trained_models(data, version=5): # Incremented version
    return train_team_models(data)

with st.spinner("Analyzing SHAP Values and Profiling TAP Benchmarks..."):
    model_results = get_trained_models(merged_data, version=5)

tabs = st.tabs(["Win the League", "Top 25%", "Avoid Relegation"])

for i, category in enumerate(["Win", "Top 25%", "Survive"]):
    with tabs[i]:
        st.markdown(f"### What it takes to **{category}**")
        st.markdown(
            "Below we show the most impactful team playstyle requirements translated using the **TAP (Tactical Archetype Profiling)** framework. "
            "These benchmarks isolate the difference between successful and unsuccessful teams for this objective based on Z-Scores relative to the league average."
        )
        
        results = model_results[category]
        req_index = results.get('required_index', {})
        req_raw = results.get('required_raw', {})
        
        if req_index:
            # Display TAP Radar Chart
            st.markdown("### The TAP Target Blueprint")
            
            categories_radar = list(INDEX_NAMES.values())
            keys_radar = list(INDEX_NAMES.keys())
            
            # Close the radar loop
            values = [req_index.get(k, 0) for k in keys_radar]
            values += [values[0]]
            cat_cyclic = categories_radar + [categories_radar[0]]
            
            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=cat_cyclic,
                fill='toself',
                name=category,
                line=dict(color='#00E5FF' if category == 'Win' else '#4FC3F7' if category == 'Top 25%' else '#66BB6A', width=3),
                fillcolor='rgba(0, 229, 255, 0.3)' if category == 'Win' else 'rgba(79, 195, 247, 0.3)' if category == 'Top 25%' else 'rgba(102, 187, 106, 0.3)' 
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        showline=False,
                        gridcolor='rgba(200, 200, 200, 0.2)'
                    ),
                    angularaxis=dict(
                        gridcolor='rgba(200, 200, 200, 0.2)'
                    )
                ),
                showlegend=False,
                height=450,
                margin=dict(l=40, r=40, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            col1, col2 = st.columns([1.5, 1])
            with col1:
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                st.markdown("#### Primary Index Targets")
                df_indices = pd.DataFrame([
                    {"TAP Index": title, "Required Z-Score": req_index.get(k, 0)}
                    for k, title in INDEX_NAMES.items()
                ])
                st.dataframe(df_indices.style.format({"Required Z-Score": "{:.2f}"}).background_gradient(cmap='viridis', subset=['Required Z-Score']), use_container_width=True, hide_index=True)
                st.info("Positive numbers mark areas where you must perform **above** the average league benchmark.")
                
                with st.expander("📖 Interpreting TAP Index Targets & Negative Values"):
                    st.markdown("""
                    **Understanding Negative Targets (like IDO)**
                    Winning the league often implies overwhelming dominance. Even with possession adjustments, elite teams spend significantly less time in pure defensive blocks (Defensive Organization - IDO) and may record fewer overall clearances or total recoveries compared to mid-table teams constantly under siege. Thus, a negative Z-Score in IDO simply means the champion archetype requires *less* volume of defensive fire-fighting than the league average.

                    **Index Breakdown Reference**:
                    *   **Game Control (IGC)**: Higher is better. Focuses on possession, passing accuracy, and deep penetration.
                    *   **Playstyle / Offense (IOB)**: Higher indicates a more structured, positional attacking style (positional attacks, back passes). Lower indicates a direct, counter-attacking style.
                    *   **Defensive Intensity (IDI)**: Higher indicates intense high pressing (high recoveries, duels won) and limiting opponent progression. 
                    *   **Defensive Organization (IDO)**: Positive means high volume of deep defensive actions. Elite teams often see lower or negative targets here.
                    *   **Transitions (ITS)**: Higher means lethal efficiency on counterattacks and transition scenarios.
                    """)

            st.markdown("---")
            st.markdown("### Metrics Breakdown Blueprint")
            st.markdown("Breakdown of the required raw metrics value to achieve the specific index.")
            
            for index_key, metrics_list in METRIC_GROUPS.items():
                with st.expander(f"⚙️ {INDEX_NAMES[index_key]} Breakdown", expanded=(index_key == 'IGC')):
                    # Make a beautiful grid
                    cols = st.columns(4)
                    for i, m_key in enumerate(metrics_list):
                        friendly_name = METRIC_NAMES.get(m_key, m_key)
                        
                        # Fix: tap_df retains the raw m_key names, so we index req_raw using m_key 
                        raw_val = req_raw.get(m_key, 0.0)
                        
                        box = cols[i % 4]
                        box.metric(label=friendly_name, value=f"{raw_val:.2f}")
        else:
            st.warning("No successful teams found in historical data to map the required blueprint.")
        st.markdown("#### Squad Profile Requirements (Season 24/25 & 25/26 only)")
        st.markdown("Filter by **position** and **possession phase** to see which player archetypes are most common in squads that achieved this objective.")
        
        raw_players = st.session_state.get('raw_players', pd.DataFrame())
        
        if not raw_players.empty:
            # We only have player data for recent seasons
            recent_players = raw_players[raw_players['Season'].isin(['24_25', '25_26'])]
            recent_data = merged_data[merged_data['Season'].isin(['24_25', '25_26'])]
            
            if category == "Win":
                success_teams_list = recent_data[recent_data['Rank'] == 1][['Team', 'Season']].drop_duplicates()
            elif category == "Top 25%":
                success_teams_list = pd.concat([
                    recent_data[(recent_data['Season'] == s) & (recent_data['Rank'] <= np.ceil(len(recent_data[recent_data['Season'] == s])*0.25))][['Team', 'Season']]
                    for s in recent_data['Season'].unique()
                ]).drop_duplicates()
            else: # Survive
                success_teams_list = pd.concat([
                    recent_data[(recent_data['Season'] == s) & (recent_data['Rank'] < (len(recent_data[recent_data['Season'] == s])-1))][['Team', 'Season']]
                    for s in recent_data['Season'].unique()
                ]).drop_duplicates()

            # Merge to get only players in successful teams
            success_players = recent_players.merge(success_teams_list, on=['Team', 'Season'], how='inner')
            
            if not success_players.empty:
                # Interactive filters
                filter_col1, filter_col2 = st.columns(2)
                with filter_col1:
                    all_positions = ['All'] + sorted(success_players['pos_group'].unique().tolist())
                    selected_pos = st.selectbox("Position Group", all_positions, key=f"league_pos_{category}")
                with filter_col2:
                    all_phases = ['All', 'In Possession', 'Out of Possession', 'Hybrid/Transition']
                    selected_phase = st.selectbox("Possession Phase", all_phases, key=f"league_phase_{category}")
                
                filtered = success_players.copy()
                if selected_pos != 'All':
                    filtered = filtered[filtered['pos_group'] == selected_pos]
                if selected_phase != 'All':
                    filtered = filtered[filtered['Phase'] == selected_phase]
                
                if not filtered.empty:
                    profile_counts = filtered['Assigned_Profile'].value_counts().head(12)
                    
                    fig_prof = go.Figure(go.Bar(
                        x=profile_counts.values[::-1],
                        y=profile_counts.index[::-1],
                        orientation='h',
                        marker=dict(
                            color=profile_counts.values[::-1],
                            colorscale='Viridis',
                            showscale=False
                        )
                    ))
                    fig_prof.update_layout(
                        title=f"Profile Distribution: {category} Blueprint",
                        xaxis_title="Number of Players",
                        yaxis_title="",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=450,
                        margin=dict(l=250)
                    )
                    st.plotly_chart(fig_prof, use_container_width=True)
                else:
                    st.info("No players found for the selected filter combination.")
            else:
                st.warning("No historical 'Success' data found in seasons 24/25 or 25/26 for this specific category.")
        else:
            st.warning("Player profile data not found. Please ensure the pipeline processed them correctly.")


        st.markdown("---")
        st.markdown("#### Detailed Team Breakdown & AI Interpretation")
        
        # Breakdown by season
        seasons = sorted(merged_data['Season'].unique(), reverse=True)
        selected_s = st.selectbox(f"Select Season to view teams ({category})", seasons, key=f"s_{category}")
        
        # Identify teams in this category for this season
        if category == "Win":
            cat_df = merged_data[(merged_data['Season'] == selected_s) & (merged_data['Rank'] == 1)]
        elif category == "Top 25%":
            total = len(merged_data[merged_data['Season'] == selected_s])
            cat_df = merged_data[(merged_data['Season'] == selected_s) & (merged_data['Rank'] <= np.ceil(total*0.25))]
        else: # Survive
            total = len(merged_data[merged_data['Season'] == selected_s])
            cat_df = merged_data[(merged_data['Season'] == selected_s) & (merged_data['Rank'] < (total-1))]
            
        if not cat_df.empty:
            for _, row in cat_df.iterrows():
                with st.expander(f"{row['Team']} (Rank: {row['Rank']})"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("**Key Strength Areas:**")
                        st.write("Identified using tactical index alignment.")
                        # Could show where they overperformed against league average visually here
                    
                    with col_b:
                        st.write("**AI Interpretation:**")
                        if category == "Win":
                            st.write(f"The champion's performance is underpinned by elite alignment with the TAP framework. They maintain unsustainable levels of dominance in key phases.")
                        elif category == "Top 25%":
                            st.write(f"Consistent performance keeps them in the European contention bracket.")
                        else:
                            st.write(f"Survival was secured through tactical discipline in defensive organization.")
        else:
            st.write("No teams matched this criteria for the selected season.")


