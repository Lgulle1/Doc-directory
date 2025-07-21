#!/bin/bash

# Doctor Directory Audit Tool Startup Script

echo "Starting Doctor Directory Audit Tool..."
echo "============================================"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if required directories exist
if [ ! -d "scrapers" ] || [ ! -d "utils" ]; then
    echo "Error: Required directories (scrapers, utils) not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Install dependencies if venv is empty
if [ ! -f "venv/pyvenv.cfg" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

echo "Starting Streamlit application..."
echo ""
echo "The application will be available at:"
echo "  - Local URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Start the Streamlit app
streamlit run main.py --server.headless=false