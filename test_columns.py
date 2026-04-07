import pandas as pd
from src.pipeline import rename_wyscout_merged_cols

file_path = "c:/Users/USER/Desktop/Rembatz Analisis/Project/How to Win Frauen Bundesliga/database/Team Stats/21_22/Team Stats Bayer Leverkusen.xlsx"

try:
    df = pd.read_excel(file_path, header=0)
    old_cols = list(df.columns)
    new_cols = rename_wyscout_merged_cols(old_cols)
    print("----- MAPPED COLUMNS -----")
    for o, n in zip(old_cols, new_cols):
        if str(o) != str(n):
            print(f"'{o}' -> '{n}'")
except Exception as e:
    print("Error:", e)
