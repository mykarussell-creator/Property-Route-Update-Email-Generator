#!/usr/bin/env python3
"""
Test flexible date parsing
"""

import pandas as pd
from datetime import datetime

def test_date_parsing(csv_file):
    print(f"\n{'='*70}")
    print(f"Testing Flexible Date Parsing: {csv_file}")
    print(f"{'='*70}\n")

    # Get today's date
    today = datetime.now().date()
    print(f"Today's date: {today}\n")

    # Read CSV
    df = pd.read_csv(csv_file)

    print("Original 'Date Added' values:")
    for val in df['Date Added'].dropna().unique():
        print(f"  - {val}")

    print("\nOriginal 'Date for Removal' values:")
    for val in df['Date for Removal'].dropna().unique():
        print(f"  - {val}")

    # Parse dates
    df['Date Added Parsed'] = pd.to_datetime(df['Date Added'], errors='coerce')
    df['Date for Removal Parsed'] = pd.to_datetime(df['Date for Removal'], errors='coerce')

    print("\n" + "─"*70)
    print("After Parsing:")
    print("─"*70)

    print("\nParsed 'Date Added' values:")
    for date in df['Date Added Parsed'].dropna().dt.date.unique():
        match = "✅ MATCH!" if date == today else "❌ No match"
        print(f"  - {date} {match}")

    print("\nParsed 'Date for Removal' values:")
    for date in df['Date for Removal Parsed'].dropna().dt.date.unique():
        match = "✅ MATCH!" if date == today else "❌ No match"
        print(f"  - {date} {match}")

    # Filter for today
    df_add_today = df[df['Date Added Parsed'].dt.date == today]
    df_remove_today = df[df['Date for Removal Parsed'].dt.date == today]

    print("\n" + "="*70)
    print(f"✅ Found {len(df_add_today)} to add and {len(df_remove_today)} to remove for today")
    print("="*70 + "\n")

if __name__ == "__main__":
    test_date_parsing('test_date_formats.csv')
