#!/usr/bin/env python3
"""
Property Route Update Email Generator - Web Interface
Run with: streamlit run routes_app.py
"""

import streamlit as st
import webbrowser
from urllib.parse import quote

# Market-to-recipients mapping
MARKET_RECIPIENTS = {
    'ATL': ['pam.mcgee@securitasinc.com', 'Keyonia.Henderson@securitasinc.com', 'atlpatrols@opendoor.com'],
    'ABQ': ['ken.nead@securitasinc.com', 'vicky.hawkins@securitasinc.com', 'abq-patrols@opendoor.com'],
    'ATX': ['mehr.enayati@securitasinc.com', 'atxpatrols@opendoor.com'],
    'BOI': ['james.kopsho@securitasinc.com', 'deepsixservicesinc@gmail.com', 'boi-patrols@opendoor.com'],
    'BOS': ['marc.cutler@securitasinc.com', 'bos-patrols@opendoor.com'],
    'CHS': ['aaron.back@securitasinc.com', 'chris.tinker@securitasinc.com', 'kenny.lancaster@securitasinc.com', 'chs-patrols@opendoor.com'],
    'CLT': ['chris.tinker@securitasinc.com', 'cltpatrols@opendoor.com'],
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
    'MSP': ['faheem.karim@securitasinc.com', 'msppatrols@opendoor.com'],
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

def generate_email(removed_addresses, added_addresses):
    """Generate a formatted email update with removed and added addresses."""
    subject = "Property Route Update"
    body = "Hi,\n\n"

    if removed_addresses:
        body += "Removed Addresses:\n\n"
        for i, address in enumerate(removed_addresses, 1):
            body += f"{i}. {address}\n"
        body += "\n"

    if added_addresses:
        body += "Added Addresses:\n\n"
        for i, address in enumerate(added_addresses, 1):
            body += f"{i}. {address}\n"
        body += "\n"

    body += "Please let me know if you have any questions.\n\nBest regards"
    return subject, body

def open_gmail_compose(subject, body, recipients=None):
    """Open Gmail compose window in browser with pre-filled content."""
    encoded_subject = quote(subject)
    encoded_body = quote(body)
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&su={encoded_subject}&body={encoded_body}"

    if recipients:
        encoded_recipients = quote(','.join(recipients))
        gmail_url += f"&to={encoded_recipients}"

    webbrowser.open(gmail_url)

# Streamlit UI
st.set_page_config(page_title="Property Route Email Generator", page_icon="🏠", layout="wide")

st.title("🏠 Property Route Update Email Generator")
st.markdown("Generate property route update emails with automatic recipient lookup")

# Market selection
col1, col2 = st.columns([1, 2])

with col1:
    market = st.selectbox(
        "Select Market",
        options=[''] + sorted(MARKET_RECIPIENTS.keys()),
        help="Choose a market to auto-fill recipients"
    )

    if market:
        recipients = MARKET_RECIPIENTS[market]
        st.success(f"✓ {len(recipients)} recipients")
        with st.expander("View Recipients"):
            for recipient in recipients:
                st.text(recipient)

with col2:
    st.markdown("### Addresses")

    removed_text = st.text_area(
        "Removed Addresses (one per line)",
        height=100,
        placeholder="123 Main St, Phoenix, AZ\n456 Oak Ave, Phoenix, AZ"
    )

    added_text = st.text_area(
        "Added Addresses (one per line)",
        height=100,
        placeholder="789 Pine Rd, Phoenix, AZ\n321 Elm St, Phoenix, AZ"
    )

# Generate button
st.markdown("---")

if st.button("📧 Generate Email & Open Gmail", type="primary", use_container_width=True):
    # Parse addresses
    removed_addresses = [addr.strip() for addr in removed_text.split('\n') if addr.strip()]
    added_addresses = [addr.strip() for addr in added_text.split('\n') if addr.strip()]

    # Validate
    if not removed_addresses and not added_addresses:
        st.error("⚠️ Please enter at least one address to add or remove")
    else:
        # Generate email
        subject, body = generate_email(removed_addresses, added_addresses)
        recipients = MARKET_RECIPIENTS.get(market) if market else None

        # Show preview
        st.success("✅ Email generated successfully!")

        with st.expander("📄 Email Preview", expanded=True):
            if recipients:
                st.markdown(f"**To:** {', '.join(recipients)}")
            st.markdown(f"**Subject:** {subject}")
            st.text(body)

        # Open Gmail
        open_gmail_compose(subject, body, recipients)
        st.info("🌐 Opening Gmail in your browser...")

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Select a market to automatically populate email recipients")
