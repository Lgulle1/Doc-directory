from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

class BaseScraper(ABC):
    """Base class for all medical directory scrapers"""
    
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.driver = None
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def setup_driver(self):
        """Initialize Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(self.timeout)
        
    def teardown_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def safe_find_element(self, by, value, default=""):
        """Safely find an element and return its text or default value"""
        try:
            element = self.driver.find_element(by, value)
            return element.text.strip()
        except NoSuchElementException:
            return default
    
    def safe_find_attribute(self, by, value, attribute, default=""):
        """Safely find an element and return its attribute or default value"""
        try:
            element = self.driver.find_element(by, value)
            return element.get_attribute(attribute) or default
        except NoSuchElementException:
            return default
    
    def wait_for_element(self, by, value, timeout=None):
        """Wait for an element to be present"""
        if timeout is None:
            timeout = self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            return None
    
    @abstractmethod
    def scrape_profile(self, url):
        """
        Scrape a doctor's profile from the given URL
        Returns dict with keys: name, phone, address, website, specialty, has_photo
        """
        pass
    
    @abstractmethod
    def get_domain(self):
        """Return the domain name this scraper handles"""
        pass
    
    def extract_profile_data(self, url):
        """Main method to extract profile data from a URL"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get(url)
            time.sleep(2)  # Allow page to load
            
            profile_data = self.scrape_profile(url)
            profile_data['profile_url'] = url
            profile_data['directory'] = self.get_domain()
            
            return profile_data
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            return {
                'name': '',
                'phone': '',
                'address': '',
                'website': '',
                'specialty': '',
                'has_photo': False,
                'profile_url': url,
                'directory': self.get_domain(),
                'error': str(e)
            }