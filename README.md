# Doctor Directory Audit Tool

A Streamlit-based Python application that audits a doctor's online presence across medical directories by searching and scraping their profiles to compare information consistency.

## Features

- **CSV Upload**: Upload doctor information (Name, Location, Website)
- **Configurable Directories**: Default medical directories + custom domain input
- **Automated Search**: Google search across specified medical directories
- **Profile Scraping**: Extract name, phone, address, website, specialty, and photo information
- **Smart Comparison**: Fuzzy matching for names and addresses, exact matching for phones and websites
- **Interactive Results**: Sortable/filterable table with match status and scores
- **Export Functionality**: Download complete audit results as CSV

## Default Medical Directories

- vitals.com (✅ Fully implemented)
- webmd.com (🔄 Generic scraper)
- healthgrades.com (🔄 Generic scraper)
- doximity.com (🔄 Generic scraper)
- usnews.com (🔄 Generic scraper)

## Setup

### Prerequisites

- Python 3.8+
- Chrome browser (for Selenium)

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run main.py
   ```

4. Open your browser to `http://localhost:8501`

## Usage

### 1. Prepare Your CSV File

Create a CSV file with the following required columns:
- **Name**: Doctor's full name (e.g., "Dr. John Smith")
- **Location**: Practice location (e.g., "Towson, MD") 
- **Website**: Doctor's website URL (e.g., "https://www.towsonortho.com/dr-john-smith")

Optional columns:
- **Phone**: Doctor's phone number (for comparison if available)

### 2. Configure Directories

- Default directories are pre-loaded
- Add custom directories in the sidebar (comma-separated)
- Example: `zocdoc.com,md.com,caredash.com`

### 3. Upload and Process

1. Upload your CSV file
2. Review the loaded data preview
3. Click "Start Audit" to begin processing
4. Monitor progress in real-time

### 4. Review Results

- **Summary Metrics**: Total profiles found, name matches, average scores
- **Detailed Table**: All scraped data with comparison results
- **Filters**: Filter by directory or match status
- **Export**: Download full results as CSV

## Technical Architecture

### Modular Design

```
├── main.py                 # Streamlit UI and main application
├── config.py              # Configuration settings
├── scrapers/              # Scraping modules
│   ├── base_scraper.py    # Abstract base class
│   ├── vitals_scraper.py  # Vitals.com implementation
│   └── scraper_factory.py # Factory pattern for scrapers
├── utils/                 # Utilities
│   ├── search_engine.py   # Google search functionality
│   └── comparison.py      # Profile comparison logic
└── requirements.txt       # Dependencies
```

### Adding New Directory Scrapers

1. Create a new scraper class inheriting from `BaseScraper`:

```python
from scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By

class NewDirectoryScraper(BaseScraper):
    def get_domain(self):
        return "newdirectory.com"
    
    def scrape_profile(self, url):
        profile_data = {
            'name': self.safe_find_element(By.CSS_SELECTOR, '.doctor-name'),
            'phone': self.safe_find_element(By.CSS_SELECTOR, '.phone'),
            'address': self.safe_find_element(By.CSS_SELECTOR, '.address'),
            'website': self.safe_find_attribute(By.CSS_SELECTOR, '.website', 'href'),
            'specialty': self.safe_find_element(By.CSS_SELECTOR, '.specialty'),
            'has_photo': bool(self.driver.find_elements(By.CSS_SELECTOR, '.photo img'))
        }
        return profile_data
```

2. Register in `scraper_factory.py`:

```python
_scrapers = {
    'vitals.com': VitalsScraper,
    'newdirectory.com': NewDirectoryScraper,  # Add here
}
```

### Comparison Logic

The tool uses intelligent comparison algorithms:

- **Names**: Fuzzy matching with 70% similarity threshold
- **Phones**: Normalized digit-only comparison
- **Addresses**: Fuzzy matching with 60% similarity threshold  
- **Websites**: Normalized URL comparison
- **Overall Score**: Average of individual field scores

## Sample Data

A `sample_doctors.csv` file is included for testing. It contains sample doctor profiles from the Maryland area.

## Limitations

- Currently optimized for Vitals.com
- Other directories use generic scraping (may have lower accuracy)
- Google search rate limits may affect large batch processing
- Requires Chrome browser for Selenium

## Troubleshooting

### Common Issues

1. **Chrome Driver Errors**: The application auto-downloads Chrome driver, but ensure Chrome browser is installed
2. **Search Rate Limits**: If Google blocks requests, try reducing batch size or adding delays
3. **Scraping Failures**: Some sites may have anti-bot protection; check logs for specific errors

### Performance Tips

- Test with small batches (≤10 doctors) first
- Use specific location information for better search results
- Monitor search query effectiveness in logs

## Contributing

To add support for new medical directories:

1. Study the target site's HTML structure
2. Create a new scraper class following the `VitalsScraper` pattern
3. Test thoroughly with real doctor profiles
4. Update the factory registration

## License

This tool is for educational and research purposes. Please respect website terms of service and rate limits when scraping.