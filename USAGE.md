# Doctor Directory Audit Tool - Quick Start Guide

## How to Run the Application

### Method 1: Using the Start Script (Recommended)
```bash
./run_app.sh
```

### Method 2: Manual Start
```bash
# Activate virtual environment
source venv/bin/activate

# Start the application
streamlit run main.py
```

## How to Use the Tool

### Step 1: Prepare Your Data
Create a CSV file with the following columns:
- **Name**: Doctor's full name (e.g., "Dr. John Smith")
- **Location**: City and state (e.g., "Towson, MD")  
- **Website**: Doctor's official website (optional)

### Step 2: Upload and Configure
1. Open the application in your browser (http://localhost:8501)
2. Upload your CSV file using the file uploader
3. (Optional) Add custom medical directory domains in the text input box
4. Click "Start Audit" to begin the process

### Step 3: Review Results
- View results in the interactive table
- Sort and filter results as needed
- Download the complete audit results as CSV

## Default Medical Directories Checked

The tool automatically searches these medical directories:
- vitals.com
- webmd.com
- healthgrades.com
- doximity.com
- usnews.com

## Sample CSV Format

```csv
Name,Location,Website
Dr. John Smith,Towson MD,https://www.towsonortho.com/dr-john-smith
Dr. Sarah Johnson,Baltimore MD,https://www.baltimorecardio.com/dr-sarah-johnson
Dr. Michael Brown,Annapolis MD,https://www.annapolisfamilymed.com/dr-michael-brown
```

## Understanding Results

The tool compares the following fields:
- **Name**: Fuzzy matching for name variations
- **Phone**: Exact matching for phone numbers
- **Address**: Fuzzy matching for address variations
- **Website**: Exact matching for website URLs
- **Specialty**: Text matching for medical specialties
- **Photo**: Boolean check for profile photo presence

## Important Notes

- The tool respects search engine rate limits with built-in delays
- Currently only Vitals.com has full scraping support implemented
- Results may vary based on search result accuracy and website structure changes
- This tool is for audit purposes only and should be used responsibly

## Troubleshooting

### Common Issues:
1. **Import errors**: Make sure virtual environment is activated
2. **Search failures**: Check internet connection and try again later
3. **Selenium errors**: Chrome browser may need to be installed for web scraping

### Getting Help:
- Check the application logs in the terminal
- Verify CSV file format matches requirements
- Ensure all dependencies are installed correctly