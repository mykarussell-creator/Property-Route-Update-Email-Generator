#!/usr/bin/env python3
"""
Test date filtering logic
"""

import pandas as pd
from datetime import datetime

def test_date_filtering(csv_file):
    print(f"\n{'='*70}")
    print(f"Testing Date Filtering with {csv_file}")
    print(f"{'='*70}\n")

    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"Today's date: {today}\n")

    # Read CSV
    df = pd.read_csv(csv_file)

    # Convert date columns to string
    df['Date Added'] = df['Date Added'].astype(str)
    df['Date for Removal'] = df['Date for Removal'].astype(str)

    # Filter for today's adds and removes
    df_add_today = df[df['Date Added'] == today]
    df_remove_today = df[df['Date for Removal'] == today]

    print(f"Total rows in CSV: {len(df)}")
    print(f"Properties to ADD today: {len(df_add_today)}")
    print(f"Properties to REMOVE today: {len(df_remove_today)}\n")

    # Group by market
    markets_with_updates = set()
    imported_data = {}

    # Process additions
    for market in df_add_today['Market'].unique():
        markets_with_updates.add(market)
        if market not in imported_data:
            imported_data[market] = {'add': [], 'remove': []}

        market_adds = df_add_today[df_add_today['Market'] == market]
        for _, row in market_adds.iterrows():
            imported_data[market]['add'].append({
                'address': row['Full Street Address (Including City, State, and Zip Code)'],
                'lockbox': row.get('Lockbox Code', ''),
                'gate': row.get('Gate Code', ''),
                'frequency': row.get('Frequency', '')
            })

    # Process removals
    for market in df_remove_today['Market'].unique():
        markets_with_updates.add(market)
        if market not in imported_data:
            imported_data[market] = {'add': [], 'remove': []}

        market_removes = df_remove_today[df_remove_today['Market'] == market]
        for _, row in market_removes.iterrows():
            imported_data[market]['remove'].append({
                'address': row['Full Street Address (Including City, State, and Zip Code)']
            })

    print(f"{'─'*70}")
    print(f"MARKETS WITH UPDATES TODAY: {', '.join(sorted(markets_with_updates))}")
    print(f"{'─'*70}\n")

    # Display data for each market
    for market in sorted(imported_data.keys()):
        data = imported_data[market]
        print(f"\n{'='*70}")
        print(f"MARKET: {market}")
        print(f"{'='*70}")

        print(f"\n📤 TO REMOVE ({len(data['remove'])}):")
        for item in data['remove']:
            print(f"  • {item['address']}")

        print(f"\n📥 TO ADD ({len(data['add'])}):")
        for item in data['add']:
            print(f"  • {item['address']}")
            if item['lockbox'] and str(item['lockbox']) != 'nan':
                print(f"    Lockbox: {item['lockbox']}")
            if item['gate'] and str(item['gate']) != 'nan':
                print(f"    Gate: {item['gate']}")
            if item['frequency'] and str(item['frequency']) != 'nan':
                print(f"    Frequency: {item['frequency']}")

    print(f"\n{'='*70}")
    print("✅ Test completed successfully!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    test_date_filtering('test_routes_today.csv')
