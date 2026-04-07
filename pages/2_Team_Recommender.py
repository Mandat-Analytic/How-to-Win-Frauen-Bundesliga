import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.models import train_team_models

st.set_page_config(page_title="Team Recommender", layout="wide")

st.title("Tactical Strategy & Player Recommendation Engine")

if 'merged_data' not in st.session_state:
    st.error("Please navigate to the Home page first to load datasets.")
    st.stop()

merged_data = st.session_state['merged_data']
raw_players = st.session_state.get('raw_players', pd.DataFrame())

# Use 25_26 Season
latest_season = "25_26"
teams_25_26 = merged_data[merged_data['Season'] == latest_season]['Team'].unique()

if len(teams_25_26) == 0:
    st.warning("No teams found for the 25_26 season. Showing all available teams.")
    teams_25_26 = merged_data['Team'].unique()

st.sidebar.markdown("### Settings")
selected_team = st.sidebar.selectbox("Select Team", options=sorted(teams_25_26))
objective = st.sidebar.radio("Objective", ["Win", "Top 25%", "Survive"])

st.markdown(f"### Diagnostics for **{selected_team}**")
st.markdown(f"**Goal**: {objective} | **Current Season Data**")

# ─── MODELS ───────────────────────────────────────────────
@st.cache_resource
def get_trained_models(data, version=5):
    return train_team_models(data)

model_results = get_trained_models(merged_data, version=5)
obj_results = model_results[objective]

# ─── TAP INDEX DATA ───────────────────────────────────────
overall_tap = model_results.get('overall_tap', pd.DataFrame())

# Locate the selected team's row in overall_tap
team_row_main = merged_data[(merged_data['Team'] == selected_team) & (merged_data['Season'] == latest_season)]
if team_row_main.empty:
    team_row_main = merged_data[merged_data['Team'] == selected_team].iloc[-1:]

team_idx = team_row_main.index[0] if not team_row_main.empty else None

INDEX_NAMES = {
    'IGC': 'Game Control',
    'IOB': 'Playstyle / Offense',
    'IDI': 'Defensive Intensity',
    'IDO': 'Defensive Organization',
    'ITS': 'Transitions'
}
index_keys = list(INDEX_NAMES.keys())

# ─── TAP RADAR COMPARISON ────────────────────────────────
st.markdown("---")
st.markdown("### TAP Blueprint Radar Comparison")

req_index = obj_results.get('required_index', {})

col_radar, col_table = st.columns([1.2, 1])

with col_radar:
    if team_idx is not None and not overall_tap.empty and team_idx in overall_tap.index:
        team_tap = overall_tap.loc[team_idx]
        
        team_vals = [team_tap.get(k, 0) for k in index_keys]
        blueprint_vals = [req_index.get(k, 0) for k in index_keys]
        labels = [INDEX_NAMES[k] for k in index_keys]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=team_vals + [team_vals[0]],
            theta=labels + [labels[0]],
            fill='toself',
            name=f'{selected_team} Current',
            line_color='#FF6B35',
            fillcolor='rgba(255, 107, 53, 0.2)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=blueprint_vals + [blueprint_vals[0]],
            theta=labels + [labels[0]],
            fill='toself',
            name=f'{objective} Blueprint',
            line_color='#1E88E5',
            fillcolor='rgba(30, 136, 229, 0.15)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, gridcolor='rgba(128,128,128,0.3)'),
                angularaxis=dict(gridcolor='rgba(128,128,128,0.3)')
            ),
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("TAP index data not available for this team. Try re-running the pipeline.")

with col_table:
    st.markdown("#### Index Gap Analysis")
    
    if team_idx is not None and not overall_tap.empty and team_idx in overall_tap.index:
        team_tap = overall_tap.loc[team_idx]
        
        gap_data = []
        for k in index_keys:
            current = team_tap.get(k, 0)
            target = req_index.get(k, 0)
            gap = target - current
            gap_data.append({
                'TAP Index': INDEX_NAMES[k],
                'Current': round(current, 2),
                'Target': round(target, 2),
                'Gap': round(gap, 2),
                'Status': '✅ Above' if current >= target else '⚠️ Below'
            })
        
        df_gap = pd.DataFrame(gap_data)
        st.dataframe(
            df_gap.style.format({'Current': '{:.2f}', 'Target': '{:.2f}', 'Gap': '{:.2f}'})
              .background_gradient(cmap='RdYlGn_r', subset=['Gap']),
            use_container_width=True, hide_index=True
        )
        
        below_indices = [d for d in gap_data if d['Status'] == '⚠️ Below']
        if below_indices:
            worst = max(below_indices, key=lambda x: abs(x['Gap']))
            st.error(f"**Priority Focus**: {worst['TAP Index']} (Gap: {worst['Gap']:+.2f})")
        else:
            st.success(f"{selected_team} already meets or exceeds the {objective} blueprint across all TAP indices!")

# ─── CURRENT ROSTER ──────────────────────────────────────
st.markdown("---")
st.markdown("### Current Roster Profile Breakdown")

if not raw_players.empty:
    team_players = raw_players[(raw_players['Team'] == selected_team) & (raw_players['Season'] == latest_season)]
    
    if team_players.empty:
        # Fallback to latest available season
        latest_avail = raw_players[raw_players['Team'] == selected_team]['Season'].max()
        if latest_avail:
            team_players = raw_players[(raw_players['Team'] == selected_team) & (raw_players['Season'] == latest_avail)]
            st.info(f"No 25/26 player data found. Showing latest available season: {latest_avail}")
    
    if not team_players.empty:
        roster_display = team_players[['Player', 'pos_group', 'Assigned_Profile', 'Phase', 'Minutes played']].copy()
        roster_display.columns = ['Player', 'Position', 'Profile Archetype', 'Possession Phase', 'Minutes Played']
        roster_display = roster_display.sort_values('Minutes Played', ascending=False).reset_index(drop=True)
        
        # Summary counters
        phase_counts = roster_display['Possession Phase'].value_counts()
        sum_cols = st.columns(3)
        for i, phase in enumerate(['In Possession', 'Out of Possession', 'Hybrid/Transition']):
            count = phase_counts.get(phase, 0)
            sum_cols[i].metric(label=phase, value=f"{count} players")
        
        st.dataframe(
            roster_display.style.format({'Minutes Played': '{:.0f}'}),
            use_container_width=True, hide_index=True, height=400
        )
    else:
        st.warning("No player data available for this team.")
else:
    st.warning("Player data not loaded. Please navigate to the Home page first.")

# ─── PROFILE GAP RECOMMENDATIONS ─────────────────────────
st.markdown("---")
st.markdown("### Recruitment Recommendations: Missing Profiles")

# Map TAP index deficiencies to player profiles that would help
TAP_TO_PROFILES = {
    'IGC': {
        'description': 'Game Control requires dominant possession and progressive passing.',
        'profiles': [
            ('DMF', 'Deep-Lying Playmaker (Regista)', 'In Possession'),
            ('CMF', 'Progressive Playmaker', 'In Possession'),
            ('CMF', 'Possession Controller', 'In Possession'),
            ('DMF', 'Organizer (Tempo Controller)', 'In Possession'),
            ('CB', 'Ball-Playing Centerback', 'In Possession'),
            ('FB', 'Inverted Fullback (Connector-Hybrid Midfielder)', 'In Possession'),
        ]
    },
    'IOB': {
        'description': 'Playstyle/Offense requires positional play and deep creative output.',
        'profiles': [
            ('CAM', 'Classic No. 10', 'In Possession'),
            ('Winger', 'Playmaking Winger', 'In Possession'),
            ('CAM', 'Deep Playmaker', 'In Possession'),
            ('CF', 'Second Striker', 'In Possession'),
            ('FB', 'Inverted Fullback (Creator-Hybrid Midfielder)', 'In Possession'),
        ]
    },
    'IDI': {
        'description': 'Defensive Intensity requires aggressive pressing and high recoveries.',
        'profiles': [
            ('DMF', 'Destroyer', 'Out of Possession'),
            ('DMF', 'Shuttlers', 'Hybrid/Transition'),
            ('CF', 'Aggressive Presser', 'Out of Possession'),
            ('Winger', 'Aggressive Presser', 'Out of Possession'),
            ('CAM', 'Aggressive Presser', 'Out of Possession'),
            ('FB', 'High-Pressing Fullback (Aggressive Presser)', 'Out of Possession'),
        ]
    },
    'IDO': {
        'description': 'Defensive Organization requires structured defensive blocks and aerial volume.',
        'profiles': [
            ('CB', 'Classic Stopper Centerback', 'Out of Possession'),
            ('CB', 'Sweeper Centerback (Covering Type)', 'Out of Possession'),
            ('DMF', 'Defensive-Anchor', 'Out of Possession'),
            ('FB', 'Defensive Fullback', 'Out of Possession'),
            ('DMF', 'Sitters', 'Out of Possession'),
            ('FB', 'Aerial Dominant Fullback', 'Out of Possession'),
        ]
    },
    'ITS': {
        'description': 'Transitions require fast counter-attacking efficiency.',
        'profiles': [
            ('Winger', 'Direct Winger', 'In Possession'),
            ('CF', 'Poacher', 'In Possession'),
            ('CMF', 'Complete Box-to-Box Midfielder', 'Hybrid/Transition'),
            ('FB', 'Counter-Attacking Fullback', 'Hybrid/Transition'),
            ('FB', 'Overlapping Fullback (Traditional Wide Runner)', 'Hybrid/Transition'),
        ]
    }
}

if team_idx is not None and not overall_tap.empty and team_idx in overall_tap.index:
    team_tap = overall_tap.loc[team_idx]
    
    # Sort deficiencies by gap magnitude (worst first)
    deficiencies = []
    for k in index_keys:
        current = team_tap.get(k, 0)
        target = req_index.get(k, 0)
        gap = target - current
        if gap > 0:  # Only show areas where improvement is needed
            deficiencies.append((k, gap))
    
    deficiencies.sort(key=lambda x: x[1], reverse=True)
    
    if deficiencies:
        for idx_key, gap in deficiencies:
            info = TAP_TO_PROFILES.get(idx_key, {})
            idx_name = INDEX_NAMES[idx_key]
            
            with st.expander(f"🎯 {idx_name} ({idx_key}) — Gap: {gap:+.2f}", expanded=(gap == deficiencies[0][1])):
                st.markdown(f"**{info.get('description', '')}**")
                
                # Check which of these profiles the team already has
                existing_profiles = set()
                if not raw_players.empty:
                    team_p = raw_players[(raw_players['Team'] == selected_team) & (raw_players['Season'] == latest_season)]
                    existing_profiles = set(team_p['Assigned_Profile'].unique())
                
                rec_data = []
                for pos, prof, phase in info.get('profiles', []):
                    has_it = prof in existing_profiles
                    rec_data.append({
                        'Position': pos,
                        'Profile': prof,
                        'Phase': phase,
                        'In Squad': '✅ Yes' if has_it else '❌ No',
                        'Priority': 'Low' if has_it else 'HIGH'
                    })
                
                df_rec = pd.DataFrame(rec_data)
                st.dataframe(df_rec, use_container_width=True, hide_index=True)
                
                missing = [r for r in rec_data if r['Priority'] == 'HIGH']
                if missing:
                    st.warning(f"🔍 **{len(missing)} profile(s) missing** that could directly improve {idx_name}.")
                else:
                    st.success(f"✅ All recommended profiles for {idx_name} are already present in the squad.")
    else:
        st.success(f"🏆 {selected_team} has no TAP index deficiencies relative to the {objective} blueprint! The squad composition is well-aligned.")
else:
    st.warning("TAP index data not available for detailed recommendations.")
