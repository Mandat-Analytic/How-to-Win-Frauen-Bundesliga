import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score

@st.cache_resource
def train_team_models(df):
    """
    Trains models to predict points based on team playstyle.
    Extracts SHAP values to explain feature importance.
    """
    # Merge stats with standings if not done
    # Identify target columns
    targets = ['Points', 'Expected points', 'Rank']
    features_cols = [c for c in df.columns if c not in targets + ['Team', 'Season', 'Matches', 'Won', 'Draw', 'Lost', 'Goals', 'Conceded goals', 'Best goalscorer'] and np.issubdtype(df[c].dtype, np.number)]
    
    # Fill NAs
    df_features = df[features_cols].fillna(0)
    
    results = {}
    
    # 1. Regression for Points
    X = df_features
    y_pts = df['Points']
    
    xgb_pts = xgb.XGBRegressor(n_estimators=100, max_depth=3, random_state=42)
    xgb_pts.fit(X, y_pts)
    
    explainer_pts = shap.TreeExplainer(xgb_pts)
    shap_values_pts = explainer_pts.shap_values(X)
    
    results['Points'] = {
        'model': xgb_pts,
        'explainer': explainer_pts,
        'shap_values': shap_values_pts,
        'features': features_cols
    }
    
    # 2. Add classification if needed, but for simplicity, we use SHAP from Points for "Win" and "Top 25%".
    # Wait, let's build explicit binary targets.
    df['is_win'] = (df['Rank'] == 1).astype(int)
    total_teams = df.groupby('Season')['Team'].transform('count')
    df['is_top_25'] = (df['Rank'] <= np.ceil(total_teams * 0.25)).astype(int)
    df['survived'] = (df['Rank'] < (total_teams - 1)).astype(int)
    
    for cat, col in [('Win', 'is_win'), ('Top 25%', 'is_top_25'), ('Survive', 'survived')]:
        y_cat = df[col]
        clf = xgb.XGBClassifier(n_estimators=50, max_depth=3, random_state=42, use_label_encoder=False, eval_metric='logloss')
        clf.fit(X, y_cat)
        expl_clf = shap.TreeExplainer(clf)
        shap_clf = expl_clf.shap_values(X)
        
        # --- NEW TAP IMPLEMENTATION ---
        # Instead of using raw features to build a blueprint, we will use TAP indices.
        results[cat] = {
            'model': clf,
            'explainer': expl_clf,
            'shap_values': shap_clf,
            'features': features_cols,
        }
        
    # CALCULATE TAP INDICES FOR ALL TEAMS
    tap_metrics = calculate_tap_targets(df)
    
    # Store required TAP profiles in results
    for cat, col in [('Win', 'is_win'), ('Top 25%', 'is_top_25'), ('Survive', 'survived')]:
        success_teams = df[df[col] == 1]
        
        if len(success_teams) > 0:
            success_indices = success_teams.index
            cat_tap = tap_metrics.loc[success_indices]
            
            # Mean for required index targets
            req_index = cat_tap[['IGC', 'IOB', 'IDI', 'IDO', 'ITS']].mean().to_dict()
            
            # Mean for raw components
            req_raw = cat_tap.drop(columns=['IGC', 'IOB', 'IDI', 'IDO', 'ITS', 'Season']).mean().to_dict()
            
            # Mean for ALL raw features (used by Team Recommender's original SHAP flow)
            req_profile = success_teams[features_cols].mean().to_dict()
            
            results[cat]['required_index'] = req_index
            results[cat]['required_raw'] = req_raw
            results[cat]['required_profile'] = req_profile
        else:
            results[cat]['required_index'] = {}
            results[cat]['required_raw'] = {}
            results[cat]['required_profile'] = {}

    results['overall_tap'] = tap_metrics
    return results

def calculate_tap_targets(df):
    """
    Given the merged processed dataframe, standardizes the TAP metrics via z-score per season,
    and calculates the TAP indices.
    """
    # Mapping logical internal TAP metric names to the actual merged_data column names
    col_map = {
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

    metric_signs = {
        'IGC': {'T_PassAcc': 1, 'T_Possession': 1, 'T_AvgPassPerPoss': 1, 'T_ProgPasses': 1, 'T_DeepCompPasses': 1},
        'IOB': {'T_PosAttacks': 1, 'T_AvgPassPerPoss': 1, 'T_BackPasses': 1, 'T_CounterAtt': -1, 'T_AvgPassLen': -1, 'T_LongPassPct': -1},
        'IDI': {'T_HighRecov': 1, 'T_PPDA': -1, 'T_DefDuelsWon': 1, 'T_SlidingTackles': 1, 'O_ProgPasses': -1},
        'IDO': {'T_Interceptions': 1, 'T_Clearances': 1, 'T_TotalRecov': 1, 'T_AerialDuelsWon': 1, 'O_ShotsOnTarget': -1, 'O_PenAreaEntries': -1},
        'ITS': {'T_CounterAtt': 1, 'T_CounterConv': 1, 'T_DeepCompPasses': 1, 'T_SmartPasses': 1, 'O_Recoveries': -1},
    }

    # Extract required raw columns to a new DF
    tap_df = pd.DataFrame(index=df.index)
    tap_df['Season'] = df['Season']
    
    for tap_key, orig_col in col_map.items():
        if orig_col in df.columns:
            tap_df[tap_key] = pd.to_numeric(df[orig_col], errors='coerce').fillna(0)
        else:
            tap_df[tap_key] = 0.0

    # Custom Issue 2: Possession-Adjusted (PAdj) Defensive Metrics
    # Formula given: PAdj_Stat = Stat / (Opponent_Possession_Percentage / 100 * 60) * 30
    # simplifies to PAdj_Stat = Stat * 50 / Opponent_Possession_Percentage
    possession_col = 'T_Possession'
    if possession_col in tap_df.columns:
        # Avoid division by zero
        opp_possession = np.clip(100 - tap_df[possession_col], 1, 99)
        team_possession = np.clip(tap_df[possession_col], 1, 99)
        
        # Adjust Team's Defensive Actions based on Opponent's Time on ball
        team_def_metrics = ['T_Interceptions', 'T_Clearances', 'T_SlidingTackles', 'T_TotalRecov', 'T_HighRecov']
        for m in team_def_metrics:
            if m in tap_df.columns:
                tap_df[m] = tap_df[m] * 50 / opp_possession
                
        # Adjust Opponent's Defensive Actions based on Team's Time on ball
        opp_def_metrics = ['O_Recoveries']
        for m in opp_def_metrics:
            if m in tap_df.columns:
                tap_df[m] = tap_df[m] * 50 / team_possession

    raw_metrics_cols = list(col_map.keys())

    # Z-score normalization per season
    z_df = tap_df.copy()
    for season in z_df['Season'].unique():
        season_mask = z_df['Season'] == season
        season_data = z_df.loc[season_mask, raw_metrics_cols]
        mu = season_data.mean()
        sigma = season_data.std().replace(0, 1) # avoid div by zero
        z_df.loc[season_mask, raw_metrics_cols] = (season_data - mu) / sigma
    
    # Fill any remaining NaNs across the board to 0
    z_df[raw_metrics_cols] = z_df[raw_metrics_cols].fillna(0)

    # Compute indices
    for idx_name, signs in metric_signs.items():
        total = pd.Series(0.0, index=tap_df.index)
        for metric, sign in signs.items():
            if metric in z_df.columns:
                total += sign * z_df[metric]
        tap_df[idx_name] = total

    return tap_df

def get_top_features_from_shap(shap_values, feature_names, top_n=10):
    val_mean = np.abs(shap_values).mean(axis=0)
    feature_importance = list(zip(feature_names, val_mean))
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    return feature_importance[:top_n]

def predict_improvements(team_row, required_profile, top_features_importances):
    """
    Given a team's current row, the blueprint (required profile averages), and the top important features (from SHAP),
    suggest the top improvements.
    """
    suggestions = []
    top_feature_names = [x[0] for x in top_features_importances]
    for feat in top_feature_names:
        current_val = team_row[feat].values[0] if isinstance(team_row, pd.DataFrame) else team_row[feat]
        req_val = required_profile[feat]
        diff = req_val - current_val
        
        # Only suggest if it's currently worse than required.
        # This is tricky because for some metrics, lower is better. 
        # But for SHAP, we generally look at the positive correlation.
        # We can extract pearson correlation to know direction.
        # For simplicity, if difference is significant, we report it.
        if abs(diff) > (req_val * 0.1) and req_val != 0:
            if diff > 0:
                direction = "Increase"
            else:
                direction = "Decrease"
            suggestions.append({'Metric': feat, 'Current': current_val, 'Target': req_val, 'Action': direction})
    return pd.DataFrame(suggestions)
