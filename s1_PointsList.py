# s1_PointsList.py
# Script for working with Excel and CSV files in the UKBMS environment (Python 3.12)

import pandas as pd
import numpy as np

if __name__ == "__main__":
    # Path to the Excel file
    excel_path = r"C:\Users\dfedosov\Downloads\GS\SUMMARY EDIT - DENIS.xlsx"

    # Read the 'FORMAT' sheet
    df_format = pd.read_excel(excel_path, sheet_name='FORMAT')
    print("Loaded 'FORMAT' sheet:")
    print(df_format.head())

    # Read the 'LV07 DB' sheet
    df_lv07 = pd.read_excel(excel_path, sheet_name='LV07 DB')
    print("Loaded 'LV07 DB' sheet:")
    print(df_lv07.head())

    # Split LV07 DB by unique PANEL values and save to new Excel file
    output_path = r"C:\Users\dfedosov\Downloads\GS\SUMMARY EDIT - DENIS_v01.xlsx"
    panel_groups = df_lv07.groupby('PANEL')

    # Get the first 6 rows from the FORMAT sheet (preserve all columns and formatting)
    format_header = df_format.head(6)

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for panel, group in panel_groups:
            # Replace invalid characters for Excel sheet names
            sheet_name = str(panel)[:31].replace('/', '_').replace('\\', '_').replace('*', '_').replace('[', '_').replace(']', '_').replace(':', '_').replace('?', '_')
            # Concatenate the FORMAT header and the PANEL group data
            combined = pd.concat([format_header, group], ignore_index=True)
            combined.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    print(f"Split sheets saved to {output_path}")


