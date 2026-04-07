import pandas as pd
import sys

file_path = "c:/Users/USER/Desktop/Rembatz Analisis/Project/How to Win Frauen Bundesliga/database/Team Standings.xlsx"

try:
    xls = pd.ExcelFile(file_path)
    print("Sheets:", xls.sheet_names)
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        print(f"--- Sheet: {sheet} ---")
        print("Columns:", list(df.columns))
        print(df.head(2))
except Exception as e:
    print("Error:", e)
