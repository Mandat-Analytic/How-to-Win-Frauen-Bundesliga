import os

# Base paths
BASE_PATH = r"C:\Users\USER\Desktop\Rembatz Analisis\TAP\Database"
ASSETS_PATH = r"c:\Users\USER\Desktop\Rembatz Analisis\TAP\assets"
OUTPUTS_PATH = r"c:\Users\USER\Desktop\Rembatz Analisis\TAP\outputs"
CACHE_PATH = r"c:\Users\USER\Desktop\Rembatz Analisis\TAP\cache"

for path in [ASSETS_PATH, OUTPUTS_PATH, CACHE_PATH]:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

# ---- TAP Metric Groups ----
# Each list contains the RAW metric keys.
# The +/- direction is applied in tap_calculator.calculate_indices().
METRIC_GROUPS = {
    'IGC': ['T_PassAcc', 'T_Possession', 'T_AvgPassPerPoss', 'T_ProgPasses', 'T_DeepCompPasses'],
    'IOB': ['T_PosAttacks', 'T_AvgPassPerPoss', 'T_BackPasses', 'T_CounterAtt', 'T_AvgPassLen', 'T_LongPassPct'],
    'IDI': ['T_HighRecov', 'T_PPDA', 'T_DefDuelsWon', 'T_SlidingTackles', 'O_ProgPasses'],
    'IDO': ['T_Interceptions', 'T_Clearances', 'T_TotalRecov', 'T_AerialDuelsWon', 'O_ShotsOnTarget', 'O_PenAreaEntries'],
    'ITS': ['T_CounterAtt', 'T_CounterConv', 'T_DeepCompPasses', 'T_SmartPasses', 'O_Recoveries'],
}

# Signs for each metric in its index (+1 = higher is better, -1 = lower is better)
METRIC_SIGNS = {
    'IGC': {'T_PassAcc': 1, 'T_Possession': 1, 'T_AvgPassPerPoss': 1, 'T_ProgPasses': 1, 'T_DeepCompPasses': 1},
    'IOB': {'T_PosAttacks': 1, 'T_AvgPassPerPoss': 1, 'T_BackPasses': 1, 'T_CounterAtt': -1, 'T_AvgPassLen': -1, 'T_LongPassPct': -1},
    'IDI': {'T_HighRecov': 1, 'T_PPDA': -1, 'T_DefDuelsWon': 1, 'T_SlidingTackles': 1, 'O_ProgPasses': -1},
    'IDO': {'T_Interceptions': 1, 'T_Clearances': 1, 'T_TotalRecov': 1, 'T_AerialDuelsWon': 1, 'O_ShotsOnTarget': -1, 'O_PenAreaEntries': -1},
    'ITS': {'T_CounterAtt': 1, 'T_CounterConv': 1, 'T_DeepCompPasses': 1, 'T_SmartPasses': 1, 'O_Recoveries': -1},
}

INDEX_NAMES = {
    'IGC': 'Squad Quality (Game Control)',
    'IOB': 'Offensive Behavior (Possessional vs Direct)',
    'IDI': 'Defensive Intensity',
    'IDO': 'Defensive Organization',
    'ITS': 'Transition Effectiveness',
}

INDEX_SHORT = {
    'IGC': 'Game Control',
    'IOB': 'Playstyle',
    'IDI': 'Def. Intensity',
    'IDO': 'Def. Organization',
    'ITS': 'Transitions',
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
    'T_HighRecov': 'High Recoveries',
    'T_PPDA': 'PPDA',
    'T_DefDuelsWon': 'Defensive Duels Won',
    'T_SlidingTackles': 'Sliding Tackles (succ.)',
    'T_Interceptions': 'Interceptions',
    'T_Clearances': 'Clearances',
    'T_TotalRecov': 'Total Recoveries',
    'T_AerialDuelsWon': 'Aerial Duels Won',
    'T_CounterConv': 'Counter-attack Conv. %',
    'T_SmartPasses': 'Smart Passes (acc.)',
    'T_MatchTempo': 'Match Tempo',
    'O_ProgPasses': 'Opp Progressive Passes',
    'O_ShotsOnTarget': 'Opp Shots on Target',
    'O_PenAreaEntries': 'Opp Penalty Area Entries',
    'O_Recoveries': 'Opp Recoveries',
    'O_Possession': 'Opp Possession %',
    'O_PPDA': 'Opp PPDA',
}

# Output performance metrics
OUTPUT_METRICS = {
    'Goals': 'Goals',
    'xG': 'xG',
    'Shots': 'Total Shots',
    'ShotsOnTarget': 'Shots on Target',
    'Crosses': 'Crosses (accurate)',
    'DeepCompPasses': 'Deep Completed Passes',
    'DeepCompCrosses': 'Deep Completed Crosses',
    'PenAreaEntries': 'Penalty Area Entries',
    'TouchesPenArea': 'Touches in Pen. Area',
    'PosAttacks': 'Positional Attacks',
    'CounterAttacks': 'Counterattacks',
    'SetPieces': 'Set Pieces',
}

OUTPUT_AGAINST_METRICS = {
    'ConcededGoals': 'Goals Conceded',
    'OppxG': 'Opp xG',
    'ShotsAgainst': 'Shots Against',
    'ShotsAgainstOT': 'Shots Against (on target)',
    'OppCrosses': 'Opp Crosses',
    'OppDeepComp': 'Opp Deep Completed Passes',
    'OppPenEntries': 'Opp Penalty Area Entries',
    'OppTouchesPen': 'Opp Touches in Pen. Area',
    'OppPosAttacks': 'Opp Positional Attacks',
    'OppCounterAtt': 'Opp Counterattacks',
    'OppSetPieces': 'Opp Set Pieces',
}

DEFAULT_NORMALIZATION = 'z_score'

# UI Colors
COLORS = {
    'bg_primary': '#0E1117',
    'bg_card': '#1A1E2E',
    'bg_glass': 'rgba(26, 30, 46, 0.7)',
    'accent_blue': '#4FC3F7',
    'accent_cyan': '#00E5FF',
    'accent_green': '#66BB6A',
    'accent_orange': '#FFA726',
    'accent_red': '#EF5350',
    'accent_purple': '#AB47BC',
    'text_primary': '#ECEFF1',
    'text_secondary': '#90A4AE',
    'gradient_start': '#4FC3F7',
    'gradient_end': '#AB47BC',
    'border': 'rgba(255,255,255,0.08)',
}
