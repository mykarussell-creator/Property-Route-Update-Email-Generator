#!/usr/bin/env python3
import argparse
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

    # Email subject
    subject = "Property Route Update"

    # Build the email body
    body = "Hi,\n\n"

    # Add removed addresses section if any
    if removed_addresses:
        body += "Removed Addresses:\n\n"
        for i, address in enumerate(removed_addresses, 1):
            body += f"{i}. {address}\n"
        body += "\n"

    # Add added addresses section if any
    if added_addresses:
        body += "Added Addresses:\n\n"
        for i, address in enumerate(added_addresses, 1):
            body += f"{i}. {address}\n"
        body += "\n"

    body += "Please let me know if you have any questions.\n\nBest regards"

    return subject, body

def open_gmail_compose(subject, body, recipients=None):
    """Open Gmail compose window in browser with pre-filled content."""
    # URL encode the subject and body
    encoded_subject = quote(subject)
    encoded_body = quote(body)

    # Build Gmail compose URL
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&su={encoded_subject}&body={encoded_body}"

    # Add recipients if provided
    if recipients:
        encoded_recipients = quote(','.join(recipients))
        gmail_url += f"&to={encoded_recipients}"

    # Open in browser
    try:
        webbrowser.open(gmail_url)
        return True
    except Exception as e:
        print(f"Error opening browser: {e}")
        return False

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Generate property route update emails with added/removed addresses.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 routes.py --market ATL --add "123 Main St" --add "456 Oak Ave"
  python3 routes.py --market PHX --remove "789 Pine Rd"
  python3 routes.py --market ATL --remove "123 Main St" --add "789 Pine Rd"
  python3 routes.py --add "321 Elm St" (no market - no recipients)
        '''
    )

    parser.add_argument('--add', action='append', metavar='ADDRESS',
                        help='Address to add (can be used multiple times)')
    parser.add_argument('--remove', action='append', metavar='ADDRESS',
                        help='Address to remove (can be used multiple times)')
    parser.add_argument('--market', type=str, metavar='CODE',
                        help='Market code (e.g., ATL, PHX, DFW) - auto-fills recipients')

    args = parser.parse_args()

    # Get lists of addresses (default to empty lists if none provided)
    removed_addresses = args.remove if args.remove else []
    added_addresses = args.add if args.add else []

    # Validate that at least one address is provided
    if not removed_addresses and not added_addresses:
        parser.print_help()
        print("\nError: At least one --add or --remove address must be provided.")
        return

    # Handle market code and get recipients
    recipients = None
    if args.market:
        market_code = args.market.upper()
        if market_code in MARKET_RECIPIENTS:
            recipients = MARKET_RECIPIENTS[market_code]
        else:
            print(f"\nWarning: Unknown market code '{args.market}'")
            print(f"Available markets: {', '.join(sorted(MARKET_RECIPIENTS.keys()))}")
            print("Proceeding without recipients...\n")

    # Generate the email
    subject, body = generate_email(removed_addresses, added_addresses)

    # Display preview
    summary = []
    if removed_addresses:
        summary.append(f"{len(removed_addresses)} removed")
    if added_addresses:
        summary.append(f"{len(added_addresses)} added")

    print(f"Email update generated ({', '.join(summary)}):")

    # Show recipients if market was specified
    if recipients:
        print(f"Sending to: {args.market.upper()} - {len(recipients)} recipients")
        for recipient in recipients:
            print(f"  - {recipient}")

    print("\n" + "=" * 60)
    print(f"Subject: {subject}\n")
    print(body)
    print("=" * 60 + "\n")

    # Open Gmail compose window
    if open_gmail_compose(subject, body, recipients):
        print("Opening Gmail compose window in browser...")
    else:
        print("Failed to open browser. Please copy the content above manually.")

if __name__ == "__main__":
    main()
