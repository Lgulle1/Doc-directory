from .vitals_scraper import VitalsScraper
from .base_scraper import BaseScraper

class ScraperFactory:
    """Factory class to create appropriate scrapers for different domains"""
    
    _scrapers = {
        'vitals.com': VitalsScraper,
        # Add more scrapers here as they're implemented
        # 'webmd.com': WebMDScraper,
        # 'healthgrades.com': HealthGradesScraper,
    }
    
    @classmethod
    def get_scraper(cls, domain):
        """Get appropriate scraper for a domain"""
        scraper_class = cls._scrapers.get(domain)
        if scraper_class:
            return scraper_class()
        else:
            # Return a generic scraper for unsupported domains
            return GenericScraper(domain)
    
    @classmethod
    def get_supported_domains(cls):
        """Get list of supported domains"""
        return list(cls._scrapers.keys())

class GenericScraper(BaseScraper):
    """Generic scraper for unsupported domains - extracts basic info"""
    
    def __init__(self, domain):
        super().__init__()
        self.domain = domain
    
    def get_domain(self):
        return self.domain
    
    def scrape_profile(self, url):
        """Basic scraping for unsupported domains"""
        profile_data = {
            'name': '',
            'phone': '',
            'address': '',
            'website': '',
            'specialty': '',
            'has_photo': False
        }
        
        try:
            # Try to find basic info using common selectors
            page_title = self.driver.title
            if page_title:
                profile_data['name'] = page_title
            
            # Look for phone numbers in page text
            import re
            page_text = self.driver.page_source
            phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            phone_match = re.search(phone_pattern, page_text)
            if phone_match:
                profile_data['phone'] = phone_match.group()
                
        except Exception as e:
            self.logger.error(f"Error in generic scraping for {url}: {str(e)}")
        
        return profile_data