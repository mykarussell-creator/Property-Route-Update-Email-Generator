#!/usr/bin/env python3
"""
Property Route Update Email Generator - Web Interface
Run with: streamlit run routes_app.py
"""

import streamlit as st
from urllib.parse import quote
import pandas as pd
import io
from datetime import datetime

# Market-to-recipients mapping
MARKET_RECIPIENTS = {
    'ATL': ['pam.mcgee@securitasinc.com', 'atlpatrols@opendoor.com'],
    'ABQ': ['ken.nead@securitasinc.com', 'vicky.hawkins@securitasinc.com', 'abq-patrols@opendoor.com'],
    'ATX': ['mehr.enayati@securitasinc.com', 'atxpatrols@opendoor.com'],
    'BOI': ['james.kopsho@securitasinc.com', 'deepsixservicesinc@gmail.com', 'boi-patrols@opendoor.com'],
    'BOS': ['marc.cutler@securitasinc.com', 'bos-patrols@opendoor.com'],
    'CHS': ['aaron.back@securitasinc.com', 'Timothy.Lockett@securitasinc.com', 'kenny.lancaster@securitasinc.com', 'chs-patrols@opendoor.com'],
    'CLT': ['Timothy.Lockett@securitasinc.com', 'sean.bachard@securitasinc.com', 'cltpatrols@opendoor.com'],
    'CVG': ['james.sherrard@securitasinc.com', 'kurt.frulla@securitasinc.com', 'cvg-patrols@opendoor.com'],
    'COS': ['michael.parsons1@securitasinc.com', 'cospatrols@opendoor.com'],
    'CUB': ['gibsontaskforce@gmail.com', 'cubpatrols@opendoor.com'],
    'CMH': ['jason.bricking@securitasinc.com', 'kurt.frulla@securitasinc.com', 'cmh-patrols@opendoor.com'],
    'DFW': ['octavio.quezada@securitasinc.com', 'carlos.cirilo@securitasinc.com', 'Ftw001.securitas@gmail.com', 'dp001.securitas@gmail.com', 'dfwpatrols@opendoor.com'],
    'DEN': ['michael.parsons1@securitasinc.com', 'denpatrols@opendoor.com'],
    'DET': ['trevor.trask@securitasinc.com', 'kurt.frulla@securitasinc.com', 'detpatrols@opendoor.com'],
    'GSO': ['vernon.meeks@securitasinc.com', 'sean.bechard@securitasinc.com', 'gsopatrols@opendoor.com'],
    'HOU': ['keith.cook@securitasinc.com', 'houpatrols@opendoor.com'],
    'IND': ['travis.mager@securitasinc.com', 'indpatrols@opendoor.com'],
    'JAX': ['david.bowling@securitasinc.com', 'jacksonvillemobilesupervisor@gmail.com', 'OrlandoMobileSupervisor1@gmail.com', 'jaxpatrols@opendoor.com'],
    'KCI': ['Robert.klostermayer@securitasinc.com', 'kcipatrols@opendoor.com'],
    'KNX': ['stacy.tislow@securitasinc.com', 'knxpatrols@opendoor.com'],
    'LAS': ['matthew.diaz@securitasinc.com', 'laspatrols@opendoor.com'],
    'LAX/RIV': ['wissam.fakhreddine@securitasinc.com', 'Julio.gonzalez@securitasinc.com', 'Charles.sunderland@securitasinc.com', 'Roy.cruz@securitasinc.com', 'laxpatrols@opendoor.com', 'rivpatrols@opendoor.com'],
    'MIA': ['ramon.santos@securitasinc.com', 'miapatrols@opendoor.com'],
    'MSP': ['Raul.Sanchez02@securitasinc.com', 'msppatrols@opendoor.com'],
    'NAS': ['stacy.tislow@securitasinc.com', 'naspatrols@opendoor.com'],
    'NYJ': ['Jason.Mahoney@securitasinc.com', 'nyjpatrols@opendoor.com'],
    'NCO': ['michael.parsons1@securitasinc.com', 'ncopatrols@opendoor.com'],
    'OKC': ['kyle.meyer@securitasinc.com', 'okcpatrols@opendoor.com'],
    'ORL': ['david.bowling@securitasinc.com', 'orlandomobilesupervisor1@gmail.com', 'orlpatrols@opendoor.com'],
    'PHX': ['ken.nead@securitasinc.com', 'vicky.hawkins@securitasinc.com', 'phxpatrols@opendoor.com'],
    'PDX': ['roy.tauala@securitasinc.com', 'Moss.Coley@securitasinc.com', 'pdxpatrols@opendoor.com'],
    'RDU': ['sean.bechard@securitasinc.com', 'rdupatrols@opendoor.com'],
    'RNO': ['Paul.Mikesell@securitasinc.com', 'rnopatrols@opendoor.com'],
    'SAC': ['alejandro.razo@securitasinc.com', 'monique.davis@securitasinc.com', 'charles.sunderland@securitasinc.com', 'sacpatrols@opendoor.com', 'sacramento.dispatch@securitasinc.com'],
    'STL': ['mike.hudson@securitasinc.com', 'stl-patrols@opendoor.com'],
    'SLC': ['john.fuller@securitasinc.com', 'slcpatrols@opendoor.com'],
    'SAT': ['mehr.enayati@securitasinc.com', 'satpatrols@opendoor.com'],
    'SAN': ['charles.sunderland@securitasinc.com', 'jason.smith2@securitasinc.com', 'sanpatrols@opendoor.com'],
    'SFO': ['eduardo.fuentes@securitasinc.com', 'charles.sunderland@securitasinc.com', 'corey.wiltshire@securitasinc.com', 'sfo-patrols@opendoor.com'],
    'TPA': ['david.bowling@securitasinc.com', 'tampamobilesupervisor@gmail.com', 'orlandomobilesupervisor1@gmail.com', 'tpapatrols@opendoor.com'],
    'TUS': ['ken.nead@securitasinc.com', 'vicky.hawkins@securitasinc.com', 'tuspatrols@opendoor.com'],
    'DC': ['kurt.frulla@securitasinc.com', 'randolph.perrin@securitasinc.com', 'dc-patrols@opendoor.com'],
}

# Initialize session state for form fields
if 'removed_addresses' not in st.session_state:
    st.session_state.removed_addresses = ''
if 'added_addresses' not in st.session_state:
    st.session_state.added_addresses = ''
if 'added_lockbox' not in st.session_state:
    st.session_state.added_lockbox = ''
if 'added_gate' not in st.session_state:
    st.session_state.added_gate = ''
if 'added_frequency' not in st.session_state:
    st.session_state.added_frequency = ''

def generate_email(removed_data, added_data, notes=None):
    """Generate a formatted email update with removed and added addresses."""
    subject = "Property Route Update"
    body = "Hi,\n\n"

    if removed_data['addresses']:
        body += "Removed Addresses:\n\n"
        for i, address in enumerate(removed_data['addresses'], 1):
            body += f"{i}. {address}\n"
        body += "\n"

    if added_data['addresses']:
        body += "Added Addresses:\n\n"
        for i, (address, lockbox, gate, freq) in enumerate(zip(
            added_data['addresses'],
            added_data['lockbox_codes'],
            added_data['gate_codes'],
            added_data['frequency']
        ), 1):
            body += f"{i}. {address}\n"
            if lockbox:
                body += f"   Lockbox Code: {lockbox}\n"
            if gate:
                body += f"   Gate Code: {gate}\n"
            if freq:
                body += f"   Frequency: {freq}\n"
        body += "\n"

    if notes:
        body += f"Notes:\n{notes}\n\n"

    body += "Please let me know if you have any questions.\n\nBest regards"
    return subject, body

# Streamlit UI
st.set_page_config(page_title="Property Route Email Generator", page_icon="🏠", layout="wide")

st.title("🏠 Property Route Update Email Generator")
st.markdown("Generate property route update emails with automatic recipient lookup")

# CSV Import Section
st.markdown("### 📁 Import CSV File")
uploaded_file = st.file_uploader("Upload a CSV file with property route updates", type=['csv'])

# Initialize imported data storage in session state
if 'imported_data' not in st.session_state:
    st.session_state.imported_data = {}

if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Show preview
        with st.expander("📊 CSV Preview", expanded=False):
            st.dataframe(df.head())

        if st.button("📥 Import Today's Updates", type="primary"):
            with st.spinner("Processing CSV..."):
                # Get today's date
                today = datetime.now().date()
                today_str = today.strftime('%Y-%m-%d')
                st.info(f"🗓️ Looking for updates dated: {today_str}")

                # Show column names for debugging
                with st.expander("🔍 Debug: CSV Columns", expanded=False):
                    st.write("Columns found in CSV:")
                    for col in df.columns:
                        st.code(f"'{col}'")

                # Parse date columns - handle multiple formats
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

                try:
                    df['Date Added Parsed'] = parse_flexible_date(df['Date Added'])
                    df['Date for Removal Parsed'] = parse_flexible_date(df['Date for Removal'])
                except Exception as e:
                    st.error(f"Error parsing dates: {str(e)}")
                    st.stop()

                # Show original and parsed dates for debugging
                with st.expander("🔍 Debug: Date Parsing", expanded=True):
                    st.write("**Original 'Date Added' values:**")
                    for orig_date in df['Date Added'].dropna().unique()[:5]:
                        st.code(f"Original: {orig_date}")

                    st.write("\n**Parsed 'Date Added' values:**")
                    unique_added = df['Date Added Parsed'].dropna().dt.date.unique()
                    for date in unique_added[:10]:
                        match = "✅ MATCH!" if date == today else "❌ No match"
                        st.code(f"{date} {match}")

                    st.write("\n**Original 'Date for Removal' values:**")
                    for orig_date in df['Date for Removal'].dropna().unique()[:5]:
                        st.code(f"Original: {orig_date}")

                    st.write("\n**Parsed 'Date for Removal' values:**")
                    unique_removed = df['Date for Removal Parsed'].dropna().dt.date.unique()
                    for date in unique_removed[:10]:
                        match = "✅ MATCH!" if date == today else "❌ No match"
                        st.code(f"{date} {match}")

                # Filter for today's adds and removes using parsed dates
                df_add_today = df[df['Date Added Parsed'].dt.date == today]
                df_remove_today = df[df['Date for Removal Parsed'].dt.date == today]

                st.write(f"📊 Found {len(df_add_today)} properties to add and {len(df_remove_today)} to remove for {today}")

                if len(df_add_today) == 0 and len(df_remove_today) == 0:
                    st.warning(f"⚠️ No properties found with today's date ({today}). Check the dates in your CSV file.")
                    st.stop()

                # Group by market
                markets_with_updates = set()
                imported_data = {}

                # Process additions by market
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

                # Process removals by market
                for market in df_remove_today['Market'].unique():
                    markets_with_updates.add(market)
                    if market not in imported_data:
                        imported_data[market] = {'add': [], 'remove': []}

                    market_removes = df_remove_today[df_remove_today['Market'] == market]
                    for _, row in market_removes.iterrows():
                        imported_data[market]['remove'].append({
                            'address': row['Full Street Address (Including City, State, and Zip Code)']
                        })

                # Store in session state
                st.session_state.imported_data = imported_data

                total_adds = len(df_add_today)
                total_removes = len(df_remove_today)

                st.success(f"✅ Imported updates for {today}")
                st.info(f"📊 Found updates for {len(markets_with_updates)} market(s): {', '.join(sorted(markets_with_updates))}")
                st.info(f"   • {total_adds} properties to add\n   • {total_removes} properties to remove")
                st.rerun()

    except Exception as e:
        st.error(f"❌ Error reading CSV: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

st.markdown("---")

# Market selection
st.markdown("### 📧 Generate Email for Market")

# If data has been imported, show only markets with updates
if st.session_state.imported_data:
    market_options = [''] + sorted(st.session_state.imported_data.keys())
    st.success(f"✅ {len(market_options)-1} market(s) have updates today")
else:
    market_options = [''] + sorted(MARKET_RECIPIENTS.keys())

market = st.selectbox(
    "Select Market to Generate Email",
    options=market_options,
    help="Choose a market - form will auto-populate with today's updates"
)

# Auto-populate from imported data if available
if market and market in st.session_state.imported_data:
    market_data = st.session_state.imported_data[market]

    # Populate removed addresses
    removed = [item['address'] for item in market_data['remove']]
    st.session_state.removed_addresses = '\n'.join(removed)

    # Populate added addresses
    added = [item['address'] for item in market_data['add']]
    st.session_state.added_addresses = '\n'.join(added)

    # Populate codes and frequency
    lockbox = [str(item['lockbox']) if item['lockbox'] and str(item['lockbox']) != 'nan' else '' for item in market_data['add']]
    st.session_state.added_lockbox = '\n'.join(lockbox)

    gate = [str(item['gate']) if item['gate'] and str(item['gate']) != 'nan' else '' for item in market_data['add']]
    st.session_state.added_gate = '\n'.join(gate)

    frequency = [str(item['frequency']) if item['frequency'] and str(item['frequency']) != 'nan' else '' for item in market_data['add']]
    st.session_state.added_frequency = '\n'.join(frequency)

    # Show what was loaded
    st.info(f"✅ **Form auto-populated for {market}**\n\n"
            f"📤 {len(removed)} properties to remove\n\n"
            f"📥 {len(added)} properties to add")

    # Show recipients
    recipients = MARKET_RECIPIENTS.get(market, [])
    if recipients:
        with st.expander(f"📨 Email will be sent to {len(recipients)} recipient(s)", expanded=False):
            for recipient in recipients:
                st.text(recipient)
    else:
        st.warning(f"⚠️ No recipients found for market: {market}")

elif market:
    # Market selected but no imported data (manual entry mode)
    recipients = MARKET_RECIPIENTS.get(market, [])
    if recipients:
        st.info(f"✓ {len(recipients)} recipients configured")
        with st.expander("View Recipients"):
            for recipient in recipients:
                st.text(recipient)
    else:
        st.warning(f"⚠️ No recipients found for market: {market}")

st.markdown("---")

# Property details form
st.markdown("### 📝 Property Details")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Removed Properties**")
    removed_text = st.text_area(
        "Addresses (one per line)",
        height=100,
        placeholder="123 Main St, Phoenix, AZ\n456 Oak Ave, Phoenix, AZ",
        key="removed_addresses"
    )

with col2:
    st.markdown("**Added Properties**")
    added_text = st.text_area(
        "Addresses (one per line)",
        height=100,
        placeholder="789 Pine Rd, Phoenix, AZ\n321 Elm St, Phoenix, AZ",
        key="added_addresses"
    )

# Additional details for added properties
st.markdown("**Additional Details for Added Properties**")
col3, col4, col5 = st.columns(3)

with col3:
    added_lockbox = st.text_area(
        "Lockbox Codes (one per line)",
        height=100,
        placeholder="#2468\n#1357",
        key="added_lockbox"
    )

with col4:
    added_gate = st.text_area(
        "Gate Codes (one per line)",
        height=100,
        placeholder="*1111#\n*2222#",
        key="added_gate"
    )

with col5:
    added_frequency = st.text_area(
        "Frequency (one per line)",
        height=100,
        placeholder="Daily\nWeekly",
        key="added_frequency"
    )

st.markdown("### Additional Notes")
notes = st.text_area(
    "Notes (optional)",
    height=100,
    placeholder="Add any additional information or special instructions...",
    key="notes"
)

# Generate button
st.markdown("---")

if st.button("📧 Generate Email & Open Gmail", type="primary", use_container_width=True):
    # Parse addresses and codes
    removed_addresses = [addr.strip() for addr in removed_text.split('\n') if addr.strip()]

    added_addresses = [addr.strip() for addr in added_text.split('\n') if addr.strip()]
    added_lockbox_codes = [code.strip() for code in added_lockbox.split('\n')]
    added_gate_codes = [code.strip() for code in added_gate.split('\n')]
    added_frequency_list = [freq.strip() for freq in added_frequency.split('\n')]

    # Pad lists to match address count
    added_lockbox_codes += [''] * (len(added_addresses) - len(added_lockbox_codes))
    added_gate_codes += [''] * (len(added_addresses) - len(added_gate_codes))
    added_frequency_list += [''] * (len(added_addresses) - len(added_frequency_list))

    # Validate
    if not removed_addresses and not added_addresses:
        st.error("⚠️ Please enter at least one address to add or remove")
    else:
        # Prepare data dictionaries
        removed_data = {
            'addresses': removed_addresses
        }

        added_data = {
            'addresses': added_addresses,
            'lockbox_codes': added_lockbox_codes,
            'gate_codes': added_gate_codes,
            'frequency': added_frequency_list
        }

        # Generate email
        subject, body = generate_email(removed_data, added_data, notes.strip() if notes else None)
        recipients = MARKET_RECIPIENTS.get(market) if market else None

        # Show preview
        st.success("✅ Email generated successfully!")

        with st.expander("📄 Email Preview", expanded=True):
            if recipients:
                st.markdown(f"**To:** {', '.join(recipients)}")
            st.markdown(f"**Subject:** {subject}")
            st.text(body)

        # Create Gmail URL
        encoded_subject = quote(subject)
        encoded_body = quote(body)
        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&su={encoded_subject}&body={encoded_body}"

        if recipients:
            encoded_recipients = quote(','.join(recipients))
            gmail_url += f"&to={encoded_recipients}"

        # Provide clickable link to open Gmail
        st.success("✅ Email generated! Click the button below to open Gmail:")
        st.markdown(f'<a href="{gmail_url}" target="_blank"><button style="background-color: #4CAF50; color: white; padding: 15px 32px; text-align: center; font-size: 16px; border: none; border-radius: 4px; cursor: pointer;">📧 Open in Gmail</button></a>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Select a market to automatically populate email recipients")
