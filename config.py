# Configuration file for the Doctor Directory Audit Tool

# Default medical directories to check
DEFAULT_DIRECTORIES = [
    "vitals.com",
    "webmd.com", 
    "healthgrades.com",
    "doximity.com",
    "usnews.com"
]

# Number of search results to check per directory
MAX_SEARCH_RESULTS = 3

# Selenium settings
WEBDRIVER_TIMEOUT = 10
PAGE_LOAD_TIMEOUT = 15

# Fields to extract and compare
PROFILE_FIELDS = [
    "name",
    "phone", 
    "address",
    "website",
    "specialty",
    "has_photo"
]