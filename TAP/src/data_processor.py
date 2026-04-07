import pandas as pd
import os
from typing import List, Dict, Tuple, Optional
import glob

class TAPDataPipeline:
    """
    Complete data processing pipeline for TAP framework.
    """
    
    def __init__(self, base_path: str):
        """
        Initialize with base database path.
        """
        self.base_path = base_path
        
    def discover_coaches(self) -> List[str]:
        """
        Scan database and return list of available coaches.
        """
        if not os.path.exists(self.base_path):
            return []
        return [d for d in os.listdir(self.base_path) if os.path.isdir(os.path.join(self.base_path, d))]
        
    def load_coach_structure(self, coach_name: str) -> Dict:
        """
        Load team and league files for a specific coach.
        """
        coach_dir = os.path.join(self.base_path, coach_name)
        team_dir = os.path.join(coach_dir, "Team")
        league_dir = os.path.join(coach_dir, "League")
        
        team_files = glob.glob(os.path.join(team_dir, "*.xlsx"))
        team_file = team_files[0] if team_files else None
        
        league_files = glob.glob(os.path.join(league_dir, "*.xlsx"))
        
        return {
            'coach_name': coach_name,
            'team_file': team_file,
            'league_files': league_files
        }
        
    def auto_detect_file_structure(self, filepath: str) -> Dict:
        """
        Automatically detect Excel file structure.
        """
        # Load the first few rows to detect structure
        df_peek = pd.read_excel(filepath, nrows=10, header=None)
        
        header_row = 0
        avg_row = None
        data_start = 1
        
        # Simple detection logic based on "avg" or "average"
        for i, row in df_peek.iterrows():
            row_str = " ".join(map(str, row.values)).lower()
            if "avg" in row_str or "average" in row_str or "mean" in row_str:
                avg_row = i
                data_start = i + 1
                break
                
        return {
            'header_row': header_row,
            'avg_row': avg_row,
            'data_start': data_start,
            'has_merged_cols': False, # Placeholder for more complex logic
            'team_opponent_pattern': True
        }
        
    def load_excel_file(self, filepath: str, sheet_name: str = 0) -> pd.DataFrame:
        """
        Load Excel and filter for valid match rows (pairs) using Date column.
        """
        structure = self.auto_detect_file_structure(filepath)
        
        # Read file
        df = pd.read_excel(filepath, sheet_name=sheet_name, header=structure['header_row'])
        
        # Filter for rows where 'Date' parses as a valid datetime
        # This removes summary rows (e.g. 'Wolfsburg', 'Opponents') and blank lines
        if 'Date' in df.columns:
            # Coerce errors will turn non-dates into NaT, then we drop them
            # We assume match rows always have a valid date
            df = df[pd.to_datetime(df['Date'], errors='coerce').notna()]
            
        return df.reset_index(drop=True)
