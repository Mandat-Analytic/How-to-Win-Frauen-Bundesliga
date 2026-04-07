import os
import re
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_DIR = BASE_DIR / "database"
TEAM_STATS_DIR = DB_DIR / "Team Stats"
PLAYER_STATS_DIR = DB_DIR / "Player Stats"
STANDINGS_FILE = DB_DIR / "Team Standings.xlsx"

def load_team_standings():
    xls = pd.ExcelFile(STANDINGS_FILE)
    all_standings = []
    for season in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=season)
        df['Season'] = season
        all_standings.append(df)
    standings_df = pd.concat(all_standings, ignore_index=True)
    return standings_df

def rename_wyscout_merged_cols(cols):
    new_cols = []
    last_base_idx = -1
    last_base_name = ""
    for i, c in enumerate(cols):
        c_str = str(c)
        if c_str.startswith("Unnamed:") or c_str.strip() == "":
            if ' / Low / Medium / High' in last_base_name:
                base = last_base_name.split(' / ')[0].strip()
                offset = i - last_base_idx
                if offset == 1: new_cols.append(base + " Low")
                elif offset == 2: new_cols.append(base + " Medium")
                elif offset == 3: new_cols.append(base + " High")
                else: new_cols.append(c_str)
            elif 'Penalty area entries' in last_base_name:
                base = "Penalty area entries"
                offset = i - last_base_idx
                if offset == 1: new_cols.append(base + " (runs)")
                elif offset == 2: new_cols.append(base + " (crosses)")
                else: new_cols.append(c_str)
            else:
                base = last_base_name.split('/')[0].strip().replace("Total ", "").strip()
                offset = i - last_base_idx
                if offset == 1: new_cols.append(f"Total {base} success")
                elif offset == 2: new_cols.append(f"Percentage {base}")
                else: new_cols.append(c_str)
        else:
            last_base_idx = i
            last_base_name = c_str
            if ' / Low / Medium / High' in c_str:
                new_cols.append("Total " + c_str.split(' / ')[0].strip())
            elif 'Penalty area entries' in c_str:
                new_cols.append("Total Penalty area entries")
            elif '/' in c_str:
                base = c_str.split('/')[0].strip()
                new_cols.append("Total " + base)
            else:
                new_cols.append(c_str)
    return new_cols

def process_single_team_stat_file(filepath):
    try:
        # Load the file
        df = pd.read_excel(filepath, header=[0])
        df.columns = rename_wyscout_merged_cols(df.columns)
        # Drop completely empty rows/cols
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Wyscout Team Stats format: Alternating rows
        # Row 0: Team, Row 1: Opponent, Row 2: Team, Row 3: Opponent...
        team_indices = list(range(0, len(df), 2))
        opp_indices = list(range(1, len(df), 2))
        
        team_df = df.iloc[team_indices].reset_index(drop=True)
        opp_df = df.iloc[opp_indices].reset_index(drop=True)
        
        numeric_cols = team_df.select_dtypes(include=[np.number]).columns
        
        # Aggregate mean per team
        team_stats = team_df[numeric_cols].mean()
        opp_stats = opp_df[numeric_cols].mean()
        opp_stats.index = ["opponent_" + str(c) for c in opp_stats.index]
        
        combined = pd.concat([team_stats, opp_stats])
        return combined.to_dict()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def load_all_team_stats():
    data = []
    if not TEAM_STATS_DIR.exists():
        return pd.DataFrame()
        
    for season_dir in TEAM_STATS_DIR.iterdir():
        if not season_dir.is_dir(): continue
        season = season_dir.name
        for filepath in season_dir.glob("Team Stats *.xlsx"):
            filename = filepath.name
            match = re.search(r"Team Stats (.+)\.xlsx", filename)
            if match:
                team_name = match.group(1).strip()
                stats_dict = process_single_team_stat_file(filepath)
                if stats_dict:
                    stats_dict['Team'] = team_name
                    stats_dict['Season'] = season
                    data.append(stats_dict)
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    standings = load_team_standings()
    print("Standings shape:", standings.shape)
    team_stats = load_all_team_stats()
    print("Team Stats shape:", team_stats.shape)
    if not team_stats.empty:
        print("Team Stats cols:", len(team_stats.columns))
        print("Sample teams:", team_stats['Team'].unique()[:5])
