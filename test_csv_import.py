#!/usr/bin/env python3
"""
Test script for CSV import functionality
Run with: python test_csv_import.py
"""

import pandas as pd

# Market-to-recipients mapping (same as in routes_app.py)
MARKET_RECIPIENTS = {
    'ATL': ['pam.mcgee@securitasinc.com', 'Keyonia.Henderson@securitasinc.com', 'atlpatrols@opendoor.com'],
    'PHX': ['ken.nead@securitasinc.com', 'vicky.hawkins@securitasinc.com', 'phxpatrols@opendoor.com'],
}

def test_csv_import(csv_file, market_filter='ALL'):
    """Test importing CSV and filtering by market"""
    print(f"\n{'='*60}")
    print(f"Testing CSV Import for Market: {market_filter}")
    print(f"{'='*60}\n")

    try:
        # Read CSV
        df = pd.read_csv(csv_file)
        print(f"✓ CSV loaded successfully")
        print(f"  Total rows: {len(df)}")
        print(f"  Columns: {', '.join(df.columns)}\n")

        # Show preview
        print("CSV Preview (first 3 rows):")
        print(df.head(3).to_string(index=False))
        print()

        # Filter by market if not ALL
        if market_filter != 'ALL':
            df_filtered = df[df['Market'] == market_filter]
            print(f"✓ Filtered to market '{market_filter}': {len(df_filtered)} rows")
        else:
            df_filtered = df
            print(f"✓ No filter applied (ALL markets): {len(df_filtered)} rows")

        # Separate by Status
        df_add = df_filtered[df_filtered['Status'] == 'Add']
        df_remove = df_filtered[df_filtered['Status'] == 'Remove']

        print(f"\n{'─'*60}")
        print("REMOVED ADDRESSES:")
        print(f"{'─'*60}")
        removed_addresses = df_remove['Full Street Address (Including City, State, and Zip Code)'].tolist()
        if removed_addresses:
            for i, addr in enumerate(removed_addresses, 1):
                print(f"{i}. {addr}")
        else:
            print("  (none)")

        print(f"\n{'─'*60}")
        print("ADDED ADDRESSES:")
        print(f"{'─'*60}")
        added_addresses = df_add['Full Street Address (Including City, State, and Zip Code)'].tolist()
        if added_addresses:
            lockbox_codes = df_add['Lockbox Code'].fillna('').tolist()
            gate_codes = df_add['Gate Code'].fillna('').tolist()
            frequency = df_add['Frequency'].fillna('').tolist()

            for i, (addr, lockbox, gate, freq) in enumerate(zip(added_addresses, lockbox_codes, gate_codes, frequency), 1):
                print(f"{i}. {addr}")
                if lockbox:
                    print(f"   Lockbox Code: {lockbox}")
                if gate:
                    print(f"   Gate Code: {gate}")
                if freq:
                    print(f"   Frequency: {freq}")
                print()
        else:
            print("  (none)")

        # Check recipients
        if market_filter in MARKET_RECIPIENTS:
            recipients = MARKET_RECIPIENTS[market_filter]
            print(f"{'─'*60}")
            print(f"EMAIL RECIPIENTS FOR {market_filter}:")
            print(f"{'─'*60}")
            for recipient in recipients:
                print(f"  • {recipient}")

        print(f"\n{'='*60}")
        print(f"✅ Test completed successfully!")
        print(f"   - Added: {len(added_addresses)} properties")
        print(f"   - Removed: {len(removed_addresses)} properties")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test with PHX market
    print("\n🧪 TEST 1: PHX Market Only")
    test_csv_import('test_routes.csv', 'PHX')

    # Test with ATL market
    print("\n🧪 TEST 2: ATL Market Only")
    test_csv_import('test_routes.csv', 'ATL')

    # Test with ALL markets
    print("\n🧪 TEST 3: ALL Markets")
    test_csv_import('test_routes.csv', 'ALL')
