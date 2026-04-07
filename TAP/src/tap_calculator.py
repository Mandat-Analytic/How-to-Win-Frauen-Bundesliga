import pandas as pd
import numpy as np
from typing import Dict, Tuple
from config import METRIC_SIGNS


class TAPMetricsCalculator:
    """
    Extract raw team + opponent metrics from match data.
    No inversions -- all values stored as-is.
    """

    def __init__(self):
        # Team-side raw column mappings
        self.team_col_map = {
            'T_PassAcc':        'Unnamed: 13',                       # pass accuracy %
            'T_Possession':     'Possession, %',
            'T_AvgPassPerPoss': 'Average passes per possession',
            'T_ProgPasses':     'Unnamed: 94',                       # progressive passes accurate
            'T_DeepCompPasses': 'Deep completed passes',
            'T_PosAttacks':     'Positional attacks / with shots',
            'T_CounterAtt':     'Counterattacks / with shots',
            'T_AvgPassLen':     'Average pass length',
            'T_BackPasses':     'Back passes / accurate',
            'T_LongPassPct':    'Long pass %',
            'T_HighRecov':      'Unnamed: 22',                       # recoveries high
            'T_PPDA':           'PPDA',
            'T_DefDuelsWon':    'Unnamed: 65',                       # defensive duels won
            'T_SlidingTackles': 'Unnamed: 71',                       # sliding tackles successful
            'T_Interceptions':  'Interceptions',
            'T_Clearances':     'Clearances',
            'T_TotalRecov':     'Recoveries / Low / Medium / High',
            'T_AerialDuelsWon': 'Unnamed: 68',                       # aerial duels won
            'T_CounterConv':    'Unnamed: 34',                       # counter-attack conversion %
            'T_SmartPasses':    'Unnamed: 97',                       # smart passes accurate
            'T_MatchTempo':     'Match tempo',
            # Output-only (not used in indices, used for radar)
            'T_Goals':          'Goals',
            'T_xG':             'xG',
            'T_Shots':          'Shots / on target',
            'T_ShotsOnTarget':  'Unnamed: 9',
            'T_Crosses':        'Unnamed: 48',
            'T_DeepCompCrosses':'Deep completed crosses',
            'T_PenAreaEntries': 'Penalty area entries (runs / crosses)',
            'T_TouchesPenArea': 'Touches in penalty area',
            'T_SetPieces':      'Set pieces / with shots',
        }

        # Opponent-side raw column mappings (read from opponent rows)
        self.opp_col_map = {
            'O_Possession':     'Possession, %',
            'O_PPDA':           'PPDA',
            'O_ProgPasses':     'Unnamed: 94',
            'O_ShotsOnTarget':  'Unnamed: 9',
            'O_PenAreaEntries': 'Penalty area entries (runs / crosses)',
            'O_Recoveries':     'Recoveries / Low / Medium / High',
            # Output-against radar
            'O_Goals':          'Goals',
            'O_xG':             'xG',
            'O_Shots':          'Shots / on target',
            'O_Crosses':        'Unnamed: 48',
            'O_DeepCompPasses': 'Deep completed passes',
            'O_TouchesPenArea': 'Touches in penalty area',
            'O_PosAttacks':     'Positional attacks / with shots',
            'O_CounterAtt':     'Counterattacks / with shots',
            'O_SetPieces':      'Set pieces / with shots',
        }

        self.sub_metric_mappings = {
            'T_PassAcc': {
                'Total': 'Passes / accurate',
                'Accurate': 'Unnamed: 12',
                'Accuracy %': 'Unnamed: 13',
            },
            'T_ProgPasses': {
                'Total': 'Progressive passes / accurate',
                'Accurate': 'Unnamed: 94',
                'Accuracy %': 'Unnamed: 95',
            },
            'T_CounterConv': {
                'Total': 'Counterattacks / with shots',
                'With Shots': 'Unnamed: 33',
                'Conversion %': 'Unnamed: 34',
            },
            'T_ShotsOnTarget': {
                'Total Shots': 'Shots / on target',
                'On Target': 'Unnamed: 9',
                'Precision %': 'Unnamed: 10',
            },
            'T_PosAttacks': {
                'Positional Attacks': 'Positional attacks / with shots',
                'With Shots': 'Unnamed: 30',
                'Efficiency %': 'Unnamed: 31',
            },
            'T_DefDuelsWon': {
                'Defensive Duels': 'Defensive duels / won',
                'Won': 'Unnamed: 65',
                'Win %': 'Unnamed: 66',
            },
            'T_TotalRecov': {
                'Total': 'Recoveries / Low / Medium / High',
                'Low': 'Unnamed: 20',
                'Medium': 'Unnamed: 21',
                'High': 'Unnamed: 22',
            },
        }

    # -------------------------------------------------------------------
    def extract_team_opponent(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        team_df = df.iloc[::2].reset_index(drop=True)
        opp_df = df.iloc[1::2].reset_index(drop=True)
        return team_df, opp_df

    def _safe_col(self, df: pd.DataFrame, col: str) -> pd.Series:
        if col in df.columns:
            return pd.to_numeric(df[col], errors='coerce')
        return pd.Series(np.nan, index=df.index)

    # -------------------------------------------------------------------
    def calculate_component_metrics(self,
                                    team_df: pd.DataFrame,
                                    opp_df: pd.DataFrame) -> pd.DataFrame:
        """Build unified metrics DataFrame -- raw values only, NO inversions."""
        metrics = pd.DataFrame()
        for key, col in self.team_col_map.items():
            metrics[key] = self._safe_col(team_df, col)
        for key, col in self.opp_col_map.items():
            metrics[key] = self._safe_col(opp_df, col)
        return metrics

    # -------------------------------------------------------------------
    def calculate_sub_metrics(self, team_df: pd.DataFrame) -> Dict:
        sub_results = {}
        for metric, mapping in self.sub_metric_mappings.items():
            sub_results[metric] = {}
            for sub_name, col in mapping.items():
                if col in team_df.columns:
                    vals = pd.to_numeric(team_df[col], errors='coerce')
                    sub_results[metric][sub_name] = vals.mean()
        return sub_results

    # -------------------------------------------------------------------
    def calculate_output_metrics(self,
                                 team_df: pd.DataFrame,
                                 opp_df: pd.DataFrame) -> Tuple[Dict, Dict]:
        output_cols = {
            'Goals': 'Goals', 'xG': 'xG',
            'Shots': 'Shots / on target', 'ShotsOnTarget': 'Unnamed: 9',
            'Crosses': 'Unnamed: 48', 'DeepCompPasses': 'Deep completed passes',
            'DeepCompCrosses': 'Deep completed crosses',
            'PenAreaEntries': 'Penalty area entries (runs / crosses)',
            'TouchesPenArea': 'Touches in penalty area',
            'PosAttacks': 'Positional attacks / with shots',
            'CounterAttacks': 'Counterattacks / with shots',
            'SetPieces': 'Set pieces / with shots',
        }
        against_cols = {
            'ConcededGoals': 'Goals', 'OppxG': 'xG',
            'ShotsAgainst': 'Shots / on target', 'ShotsAgainstOT': 'Unnamed: 9',
            'OppCrosses': 'Unnamed: 48', 'OppDeepComp': 'Deep completed passes',
            'OppPenEntries': 'Penalty area entries (runs / crosses)',
            'OppTouchesPen': 'Touches in penalty area',
            'OppPosAttacks': 'Positional attacks / with shots',
            'OppCounterAtt': 'Counterattacks / with shots',
            'OppSetPieces': 'Set pieces / with shots',
        }

        output = {}
        for key, col in output_cols.items():
            s = self._safe_col(team_df, col)
            output[key] = round(float(s.mean()), 2) if not s.isna().all() else 0.0

        against = {}
        for key, col in against_cols.items():
            s = self._safe_col(opp_df, col)
            against[key] = round(float(s.mean()), 2) if not s.isna().all() else 0.0

        return output, against


# ======================================================================
class TAPIndexCalculator:
    """
    Z-score normalise raw metrics against the league, then compute
    5 TAP indices using explicit +/- signs from METRIC_SIGNS.
    """

    def __init__(self, normalization_method: str = 'z_score'):
        self.normalization_method = normalization_method

    def normalize_league_relative(self, team_metrics, league_metrics: pd.DataFrame) -> pd.DataFrame:
        league_mean = league_metrics.mean()
        league_std = league_metrics.std().replace(0, 1)
        return (team_metrics - league_mean) / league_std

    def calculate_indices(self, z_metrics: pd.DataFrame) -> pd.DataFrame:
        """
        Compute indices by summing signed z-scores.
        sign = +1 means higher raw value is better for the index.
        sign = -1 means lower raw value is better (e.g. PPDA, opp metrics).
        """
        z = z_metrics.fillna(0)
        indices = pd.DataFrame(index=z.index)

        for idx_name, signs in METRIC_SIGNS.items():
            total = pd.Series(0.0, index=z.index)
            for metric, sign in signs.items():
                if metric in z.columns:
                    total += sign * z[metric]
            indices[idx_name] = total

        return indices

    def calculate_percentiles(self,
                              team_indices: pd.Series,
                              league_indices: pd.DataFrame) -> Dict[str, float]:
        pcts = {}
        for idx in team_indices.index:
            if idx in league_indices.columns:
                rank = (league_indices[idx] < team_indices[idx]).mean() * 100
                pcts[idx] = round(rank, 1)
        return pcts

    def calculate_similarity_score(self,
                                   team_indices: pd.Series,
                                   reference_indices: pd.Series) -> float:
        return float(np.sqrt(np.sum((team_indices - reference_indices) ** 2)))

    def classify_similarity(self, score: float) -> str:
        if score < 3: return "Very Similar"
        if score < 5: return "Similar"
        if score < 7: return "Moderately Different"
        return "Very Different"
