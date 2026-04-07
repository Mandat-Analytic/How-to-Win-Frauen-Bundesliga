import os
import pandas as pd
import numpy as np
from pathlib import Path
from src.forward_profiles import CF_PROFILES, WINGER_PROFILES, CAM_PROFILES
from src.midfielder_profiles import DMF_PROFILES, CMF_PROFILES
from src.defender_profiles import CB_PROFILES, FB_PROFILES
from src.goalkeeper_profiles import GK_PROFILES

BASE_DIR = Path(__file__).parent.parent
PLAYER_STATS_DIR = BASE_DIR / "database" / "Player Stats"

# Categorize Profiles into Phases
IN_POSSESSION_PROFILES = [
    "Target Man", "Poacher", "Complete Forward", "Playmaking Winger", "Direct Winger", "Hybrid Winger",
    "Classic No. 10", "Deep Playmaker", "Deep-Lying Playmaker (Regista)", "Organizer (Tempo Controller)",
    "Connector (Link Play Facilitator)", "Progressive Playmaker", "Possession Controller", "Attacking Midfielder",
    "Ball-Playing Centerback", "Inverted Fullback (Connector-Hybrid Midfielder)", 
    "Inverted Fullback (Creator-Hybrid Midfielder)", "Sweeper Keeper (Build-Up Oriented)", 
    "Long Distributor Goalkeeper", "Safe Circulator (Possession Retainer)"
]

OUT_OF_POSSESSION_PROFILES = [
    "Aggressive Presser", "Passive Presser", "Destroyer", "Defensive-Anchor", "Sitters",
    "Classic Stopper Centerback", "Aggressive Centerback (Front-footed)", "Sweeper Centerback (Covering Type)",
    "Defensive Fullback", "High-Pressing Fullback (Aggressive Presser)", "Aerial Dominant Fullback",
    "Shot Stopper (Reflex-Based)", "Commanding Area Keeper", "Low-Block Survival Keeper"
]

HYBRID_PROFILES = [
    "Second Striker", "Box-to-Box Holding Midfielder (Hybrid 6/8)", "Shuttlers", "Complete Box-to-Box Midfielder",
    "Overlapping Fullback (Traditional Wide Runner)", "Counter-Attacking Fullback"
]

def get_profile_phase(profile_name):
    if profile_name in IN_POSSESSION_PROFILES: return "In Possession"
    if profile_name in OUT_OF_POSSESSION_PROFILES: return "Out of Possession"
    if profile_name in HYBRID_PROFILES: return "Hybrid/Transition"
    return "Unknown Phase"

# Merge profiles
ALL_PROFILES = {
    'CF': CF_PROFILES,
    'Winger': WINGER_PROFILES,
    'CAM': CAM_PROFILES,
    'DMF': DMF_PROFILES,
    'CMF': CMF_PROFILES,
    'CB': CB_PROFILES,
    'FB': FB_PROFILES,
    'GK': GK_PROFILES
}

def clean_column_name(col):
    return str(col).strip()

def map_position(pos_str):
    pos = str(pos_str).upper()
    if any(x in pos for x in ['CF', 'ST']): return 'CF'
    if any(x in pos for x in ['LW', 'RW', 'LWF', 'RWF']): return 'Winger'
    if 'AM' in pos: return 'CAM'
    if 'DM' in pos: return 'DMF'
    if 'CM' in pos: return 'CMF'
    if 'CB' in pos: return 'CB'
    if any(x in pos for x in ['LB', 'RB', 'LWB', 'RWB']): return 'FB'
    if 'GK' in pos: return 'GK'
    return 'UNKNOWN'

def score_player(row, position_group):
    profiles = ALL_PROFILES.get(position_group, {})
    if not profiles:
        return "Generic"
    
    best_profile = "Generic"
    best_score = -float('inf')
    
    # We expect the dataframe columns to have been cleaned already, but wyscout player columns 
    # might slightly differ. We will do a generic matching.
    for prof_name, data in profiles.items():
        weights = data.get('weights', {})
        score = 0
        for metric, weight in weights.items():
            # match metric
            # since wyscout player stats have very specific column names like "Goals per 90" 
            # we try to find it in row index
            if metric in row:
                val = row[metric]
                # Z-scored value should Ideally be used, but since we didn't calculate z-score for each metric yet,
                # let's just use raw * weight for simplicity, or assume row has z-scores.
                # Actually, raw * weight is biased towards large metrics.
                # If row contains z-scores (e.g. metric + '_z'), use that!
                z_metric = f"{metric}_z"
                if z_metric in row:
                    val = row[z_metric]
                if pd.notna(val):
                    score += float(val) * float(weight)
        if score > best_score:
            best_score = score
            best_profile = prof_name
            
    return best_profile

def load_and_score_players():
    # Load all files, calculate z-scores per position per season, then assign profiles
    all_players = []
    
    if not PLAYER_STATS_DIR.exists():
        return pd.DataFrame()
        
    for season_dir in PLAYER_STATS_DIR.iterdir():
        if not season_dir.is_dir(): continue
        season = season_dir.name
        
        for filepath in season_dir.glob("*.xlsx"):
            try:
                df = pd.read_excel(filepath)
                df['Season'] = season
                
                # Identify Team column
                team_col = [c for c in df.columns if 'team' in str(c).lower()]
                if team_col:
                    df['Team'] = df[team_col[0]]
                else:
                    df['Team'] = "Unknown"
                
                pos_col = [c for c in df.columns if 'position' in str(c).lower()]
                if not pos_col: continue
                
                df['pos_group'] = df[pos_col[0]].apply(map_position)
                
                # Calculate z-scores for all numeric columns
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    df[f"{col}_z"] = (df[col] - df[col].mean()) / (df[col].std() + 1e-9)
                
                # Extract Minutes Played safely
                min_col = [c for c in df.columns if 'minutes played' in str(c).lower()]
                df['Minutes played'] = df[min_col[0]] if min_col else 0
                df['Minutes played'] = pd.to_numeric(df['Minutes played'], errors='coerce').fillna(0)
                
                # Score players
                df['Assigned_Profile'] = df.apply(lambda r: score_player(r, r['pos_group']), axis=1)
                df['Phase'] = df['Assigned_Profile'].apply(get_profile_phase)
                
                all_players.append(df[['Team', 'Season', 'Player', 'Assigned_Profile', 'pos_group', 'Phase', 'Minutes played']])
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
                
    if not all_players:
        return pd.DataFrame()
        
    players_df = pd.concat(all_players, ignore_index=True)
    return players_df

def get_squad_profiles(players_df):
    if players_df.empty:
        return pd.DataFrame()
    # Pivot to get count of each profile per team per season
    pivot = pd.crosstab([players_df['Team'], players_df['Season']], players_df['Assigned_Profile'])
    pivot = pivot.reset_index()
    # Prepend Profiler_ to columns
    profile_cols = [c for c in pivot.columns if c not in ['Team', 'Season']]
    pivot = pivot.rename(columns={c: f"Prof_{c}" for c in profile_cols})
    return pivot

if __name__ == "__main__":
    pdf = load_and_score_players()
    if not pdf.empty:
        sq = get_squad_profiles(pdf)
        print("Squad Profiles:")
        print(sq.head())
    else:
        print("No players loaded.")
