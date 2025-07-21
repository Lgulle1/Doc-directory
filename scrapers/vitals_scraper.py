from selenium.webdriver.common.by import By
from .base_scraper import BaseScraper
import re

class VitalsScraper(BaseScraper):
    """Scraper for Vitals.com doctor profiles"""
    
    def get_domain(self):
        return "vitals.com"
    
    def scrape_profile(self, url):
        """Scrape doctor profile data from Vitals.com"""
        profile_data = {
            'name': '',
            'phone': '',
            'address': '',
            'website': '',
            'specialty': '',
            'has_photo': False
        }
        
        try:
            # Doctor name - try multiple selectors
            name_selectors = [
                'h1[data-qa="doctor-name"]',
                'h1.doctor-name',
                '.provider-name h1',
                'h1',
                '.doctor-profile-name'
            ]
            
            for selector in name_selectors:
                name = self.safe_find_element(By.CSS_SELECTOR, selector)
                if name:
                    profile_data['name'] = name
                    break
            
            # Phone number - look for various phone patterns
            phone_selectors = [
                '[data-qa="phone-number"]',
                '.phone-number',
                '.contact-phone',
                '.provider-phone'
            ]
            
            for selector in phone_selectors:
                phone = self.safe_find_element(By.CSS_SELECTOR, selector)
                if phone:
                    # Clean up phone number
                    phone_clean = re.sub(r'[^\d\-\(\)\s\+]', '', phone)
                    if phone_clean:
                        profile_data['phone'] = phone_clean.strip()
                        break
            
            # If no phone found in specific elements, search page text
            if not profile_data['phone']:
                page_text = self.driver.page_source
                phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
                phone_match = re.search(phone_pattern, page_text)
                if phone_match:
                    profile_data['phone'] = phone_match.group()
            
            # Address
            address_selectors = [
                '[data-qa="practice-address"]',
                '.practice-address',
                '.provider-address',
                '.office-address',
                '.address'
            ]
            
            for selector in address_selectors:
                address = self.safe_find_element(By.CSS_SELECTOR, selector)
                if address:
                    profile_data['address'] = address
                    break
            
            # Website
            website_selectors = [
                'a[data-qa="website-link"]',
                'a.website-link',
                'a[href*="http"]:contains("website")',
                '.provider-website a'
            ]
            
            for selector in website_selectors:
                website = self.safe_find_attribute(By.CSS_SELECTOR, selector, 'href')
                if website and 'http' in website:
                    profile_data['website'] = website
                    break
            
            # Specialty
            specialty_selectors = [
                '[data-qa="specialty"]',
                '.specialty',
                '.provider-specialty',
                '.doctor-specialty',
                '.medical-specialty'
            ]
            
            for selector in specialty_selectors:
                specialty = self.safe_find_element(By.CSS_SELECTOR, selector)
                if specialty:
                    profile_data['specialty'] = specialty
                    break
            
            # Check for profile photo
            photo_selectors = [
                '.doctor-photo img',
                '.provider-photo img',
                '.profile-photo img',
                'img[alt*="Dr."]',
                'img[alt*="doctor"]'
            ]
            
            for selector in photo_selectors:
                try:
                    photo_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if photo_element:
                        src = photo_element.get_attribute('src')
                        if src and 'placeholder' not in src.lower() and 'default' not in src.lower():
                            profile_data['has_photo'] = True
                            break
                except:
                    continue
            
        except Exception as e:
            self.logger.error(f"Error scraping Vitals profile {url}: {str(e)}")
        
        return profile_data