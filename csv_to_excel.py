#!/usr/bin/env python3
"""
CSV to Excel Converter
Combines all CSV files from csv_output/ directory into a single Excel file
with each CSV as a separate worksheet.
"""

import pandas as pd
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def csv_to_excel(csv_directory='csv_output', output_file='All_Data.xlsx'):
    """
    Convert all CSV files in the specified directory to sheets in an Excel file.
    
    Args:
        csv_directory (str): Directory containing CSV files
        output_file (str): Name of the output Excel file
    """
    
    # Get the directory path
    script_dir = Path(__file__).parent
    csv_dir = script_dir / csv_directory
    output_path = script_dir / "data" / output_file

    # Check if directory exists
    if not csv_dir.exists():
        logger.error(f"Directory {csv_dir} does not exist")
        return False
    
    # Get all CSV files
    csv_files = list(csv_dir.glob('*.csv'))
    
    if not csv_files:
        logger.warning(f"No CSV files found in {csv_dir}")
        return False
    
    logger.info(f"Found {len(csv_files)} CSV files to process")
    
    # Create Excel writer object
    try:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            
            for csv_file in sorted(csv_files):
                try:
                    # Read CSV file
                    logger.info(f"Processing {csv_file.name}")
                    df = pd.read_csv(csv_file)
                    
                    # Create sheet name from filename (remove .csv extension)
                    sheet_name = csv_file.stem
                    
                    # Excel sheet names have a 31 character limit
                    if len(sheet_name) > 31:
                        sheet_name = sheet_name[:31]
                        logger.warning(f"Sheet name truncated to: {sheet_name}")
                    
                    # Write to Excel sheet
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    logger.info(f"Successfully wrote {len(df)} rows to sheet '{sheet_name}'")
                    
                except Exception as e:
                    logger.error(f"Error processing {csv_file.name}: {str(e)}")
                    continue
        
        logger.info(f"Successfully created Excel file: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error creating Excel file: {str(e)}")
        return False

def main():
    """Main function to run the CSV to Excel conversion."""
    
    print("CSV to Excel Converter")
    print("=" * 50)
    
    # Run the conversion
    success = csv_to_excel("data/csv_output")
    
    if success:
        print("\n✅ Conversion completed successfully!")
        print(f"Output file: All_Data.xlsx")
    else:
        print("\n❌ Conversion failed. Check the logs above for details.")

if __name__ == "__main__":
    main()