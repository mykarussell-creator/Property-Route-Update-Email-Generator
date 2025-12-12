#!/bin/bash
# Launch the Property Route Email Generator web app

echo "Starting Property Route Email Generator..."
echo "The app will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m streamlit run routes_app.py
