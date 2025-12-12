# Property Route Email Generator

A web application for generating property route update emails with automatic recipient lookup by market.

## Installation

1. Install Streamlit:
```bash
pip3 install -r requirements.txt
```

## Running the Application

Start the web interface:
```bash
streamlit run routes_app.py
```

This will automatically open your browser to `http://localhost:8501`

## Using the Web Interface

1. **Select Market** - Choose from 42 markets (ATL, PHX, DFW, etc.)
   - Recipients are automatically populated based on market
2. **Enter Addresses**
   - Add addresses to remove (one per line)
   - Add addresses to add (one per line)
3. **Click "Generate Email"**
   - See a preview of the email
   - Gmail automatically opens with everything pre-filled

## Sharing with Others

To share this application:

1. **Share the folder** containing:
   - `routes_app.py`
   - `requirements.txt`
   - `README.md`

2. **Recipients install and run**:
   ```bash
   pip3 install -r requirements.txt
   streamlit run routes_app.py
   ```

## Command Line Version

If you prefer the command line, use `routes.py`:
```bash
python3 routes.py --market ATL --add "123 Main St" --remove "456 Oak Ave"
```

## Supported Markets

42 markets: ABQ, ATL, ATX, BOI, BOS, CHS, CLT, CMH, COS, CUB, CVG, DC, DEN, DET, DFW, GSO, HOU, IND, JAX, KCI, KNX, LAS, LAX/RIV, MIA, MSP, NAS, NCO, NYJ, OKC, ORL, PDX, PHX, RDU, RNO, SAC, SAN, SAT, SFO, SLC, STL, TPA, TUS
