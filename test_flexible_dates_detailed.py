#!/usr/bin/env python3
"""
Test flexible date parsing with details
"""

import pandas as pd
from datetime import datetime

csv_file = 'test_date_formats.csv'
today = datetime.now().date()

print(f"Today's date: {today}\n")

# Read CSV
df = pd.read_csv(csv_file)

# Parse dates
df['Date Added Parsed'] = pd.to_datetime(df['Date Added'], errors='coerce')
df['Date for Removal Parsed'] = pd.to_datetime(df['Date for Removal'], errors='coerce')

print("Row-by-row analysis:")
print("="*70)

for idx, row in df.iterrows():
    print(f"\nRow {idx + 1}:")
    print(f"  Market: {row['Market']}")
    print(f"  Address: {row['Full Street Address (Including City, State, and Zip Code)']}")
    print(f"  Date Added (original): {row['Date Added']}")
    print(f"  Date Added (parsed): {row['Date Added Parsed']}")
    if pd.notna(row['Date Added Parsed']):
        parsed_date = row['Date Added Parsed'].date()
        match = "✅ MATCH" if parsed_date == today else "❌ NO MATCH"
        print(f"  Date Added (as date): {parsed_date} {match}")
    print(f"  Date for Removal (original): {row['Date for Removal']}")
    print(f"  Date for Removal (parsed): {row['Date for Removal Parsed']}")
    if pd.notna(row['Date for Removal Parsed']):
        parsed_date = row['Date for Removal Parsed'].date()
        match = "✅ MATCH" if parsed_date == today else "❌ NO MATCH"
        print(f"  Date for Removal (as date): {parsed_date} {match}")

# Filter
df_add_today = df[df['Date Added Parsed'].dt.date == today]
df_remove_today = df[df['Date for Removal Parsed'].dt.date == today]

print("\n" + "="*70)
print(f"Filtered results:")
print(f"  Properties to ADD today: {len(df_add_today)}")
print(f"  Properties to REMOVE today: {len(df_remove_today)}")
