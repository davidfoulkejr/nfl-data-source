#!/usr/bin/env python3
"""
Simple CSV to Excel Converter
A minimal script to convert all CSV files in csv_output/ to a single Excel file.
"""

import pandas as pd
import os
from pathlib import Path

def convert_csvs_to_excel():
    """Convert all CSV files in csv_output/ to Excel sheets."""
    
    # Set up paths
    csv_dir = Path('csv_output')
    output_file = 'NFL_Data_All_Sheets.xlsx'
    
    # Get all CSV files
    csv_files = list(csv_dir.glob('*.csv'))
    
    print(f"Found {len(csv_files)} CSV files to convert...")
    
    # Create Excel file with multiple sheets
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for csv_file in sorted(csv_files):
            print(f"Converting {csv_file.name}...")
            
            # Read CSV and write to Excel sheet
            df = pd.read_csv(csv_file)
            sheet_name = csv_file.stem  # filename without extension
            
            # Excel sheet names must be <= 31 characters
            if len(sheet_name) > 31:
                sheet_name = sheet_name[:31]
            
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"\n✅ Successfully created {output_file}")
    print(f"📊 Total sheets: {len(csv_files)}")

if __name__ == "__main__":
    convert_csvs_to_excel()