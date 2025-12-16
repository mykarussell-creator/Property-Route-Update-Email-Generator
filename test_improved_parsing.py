#!/usr/bin/env python3
"""
Test improved flexible date parsing
"""

import pandas as pd
from datetime import datetime

def parse_flexible_date(date_series):
    """Parse dates trying multiple formats"""
    # First try pandas automatic parsing
    parsed = pd.to_datetime(date_series, errors='coerce')

    # For any that failed, try specific formats
    failed_mask = parsed.isna() & date_series.notna()
    if failed_mask.any():
        formats_to_try = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%m/%d/%y',
            '%Y-%m-%d %H:%M:%S',
            '%m/%d/%Y %H:%M:%S',
            '%m/%d/%Y %H:%M',
            '%d/%m/%Y',
            '%Y/%m/%d'
        ]
        for fmt in formats_to_try:
            still_failed = parsed.isna() & date_series.notna()
            if not still_failed.any():
                break
            try:
                parsed[still_failed] = pd.to_datetime(date_series[still_failed], format=fmt, errors='coerce')
            except:
                continue
    return parsed

csv_file = 'test_date_formats.csv'
today = datetime.now().date()

print(f"Today's date: {today}\n")

# Read CSV
df = pd.read_csv(csv_file)

# Parse dates with improved function
df['Date Added Parsed'] = parse_flexible_date(df['Date Added'])
df['Date for Removal Parsed'] = parse_flexible_date(df['Date for Removal'])

print("Row-by-row analysis:")
print("="*70)

for idx, row in df.iterrows():
    print(f"\nRow {idx + 1}: {row['Market']} - {row['Full Street Address (Including City, State, and Zip Code)']}")
    print(f"  Date Added (original): '{row['Date Added']}'")
    if pd.notna(row['Date Added Parsed']):
        parsed_date = row['Date Added Parsed'].date()
        match = "✅ MATCH" if parsed_date == today else f"❌ {parsed_date}"
        print(f"  Date Added (parsed): {match}")
    else:
        print(f"  Date Added (parsed): ❌ FAILED TO PARSE")

    if pd.notna(row['Date for Removal']):
        print(f"  Date for Removal (original): '{row['Date for Removal']}'")
        if pd.notna(row['Date for Removal Parsed']):
            parsed_date = row['Date for Removal Parsed'].date()
            match = "✅ MATCH" if parsed_date == today else f"❌ {parsed_date}"
            print(f"  Date for Removal (parsed): {match}")
        else:
            print(f"  Date for Removal (parsed): ❌ FAILED TO PARSE")

# Filter
df_add_today = df[df['Date Added Parsed'].dt.date == today]
df_remove_today = df[df['Date for Removal Parsed'].dt.date == today]

print("\n" + "="*70)
print(f"✅ Properties to ADD today: {len(df_add_today)}")
print(f"✅ Properties to REMOVE today: {len(df_remove_today)}")
print("="*70)
