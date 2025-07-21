import re
from difflib import SequenceMatcher
import logging

class ProfileComparator:
    """Compare scraped profile data with original CSV data"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def normalize_text(self, text):
        """Normalize text for comparison"""
        if not text:
            return ""
        
        # Convert to lowercase and remove extra whitespace
        normalized = re.sub(r'\s+', ' ', str(text).lower().strip())
        
        # Remove common punctuation
        normalized = re.sub(r'[.,;:!?()"]', '', normalized)
        
        return normalized
    
    def normalize_phone(self, phone):
        """Normalize phone number for comparison"""
        if not phone:
            return ""
        
        # Extract only digits
        digits_only = re.sub(r'[^\d]', '', str(phone))
        
        # Handle US phone numbers
        if len(digits_only) == 11 and digits_only.startswith('1'):
            digits_only = digits_only[1:]  # Remove country code
        
        return digits_only
    
    def similarity_score(self, text1, text2):
        """Calculate similarity score between two text strings"""
        normalized1 = self.normalize_text(text1)
        normalized2 = self.normalize_text(text2)
        
        if not normalized1 or not normalized2:
            return 0.0
        
        return SequenceMatcher(None, normalized1, normalized2).ratio()
    
    def compare_names(self, original_name, scraped_name, threshold=0.7):
        """Compare doctor names with fuzzy matching"""
        if not original_name or not scraped_name:
            return "Missing", 0.0
        
        score = self.similarity_score(original_name, scraped_name)
        
        if score >= threshold:
            return "Match", score
        else:
            return "Mismatch", score
    
    def compare_phones(self, original_phone, scraped_phone):
        """Compare phone numbers"""
        if not original_phone and not scraped_phone:
            return "Missing", 1.0
        
        if not original_phone or not scraped_phone:
            return "Missing", 0.0
        
        norm_original = self.normalize_phone(original_phone)
        norm_scraped = self.normalize_phone(scraped_phone)
        
        if norm_original == norm_scraped:
            return "Match", 1.0
        else:
            return "Mismatch", 0.0
    
    def compare_addresses(self, original_address, scraped_address, threshold=0.6):
        """Compare addresses with location-aware fuzzy matching"""
        if not original_address and not scraped_address:
            return "Missing", 1.0
        
        if not original_address or not scraped_address:
            return "Missing", 0.0
        
        score = self.similarity_score(original_address, scraped_address)
        
        if score >= threshold:
            return "Match", score
        else:
            return "Mismatch", score
    
    def compare_websites(self, original_website, scraped_website):
        """Compare website URLs"""
        if not original_website and not scraped_website:
            return "Missing", 1.0
        
        if not original_website or not scraped_website:
            return "Missing", 0.0
        
        # Normalize URLs
        orig_clean = self.normalize_text(original_website.replace('http://', '').replace('https://', '').replace('www.', ''))
        scraped_clean = self.normalize_text(scraped_website.replace('http://', '').replace('https://', '').replace('www.', ''))
        
        if orig_clean == scraped_clean:
            return "Match", 1.0
        else:
            return "Mismatch", 0.0
    
    def compare_profiles(self, original_data, scraped_data):
        """
        Compare complete profile data
        Returns dict with comparison results for each field
        """
        results = {
            'doctor_name': original_data.get('Name', ''),
            'original_location': original_data.get('Location', ''),
            'original_website': original_data.get('Website', ''),
            'directory': scraped_data.get('directory', ''),
            'profile_url': scraped_data.get('profile_url', ''),
            'comparisons': {}
        }
        
        # Compare name
        name_result, name_score = self.compare_names(
            original_data.get('Name', ''),
            scraped_data.get('name', '')
        )
        results['comparisons']['name'] = {
            'status': name_result,
            'score': name_score,
            'original': original_data.get('Name', ''),
            'scraped': scraped_data.get('name', '')
        }
        
        # Compare phone (if original has phone data)
        if 'Phone' in original_data:
            phone_result, phone_score = self.compare_phones(
                original_data.get('Phone', ''),
                scraped_data.get('phone', '')
            )
            results['comparisons']['phone'] = {
                'status': phone_result,
                'score': phone_score,
                'original': original_data.get('Phone', ''),
                'scraped': scraped_data.get('phone', '')
            }
        
        # Compare website
        website_result, website_score = self.compare_websites(
            original_data.get('Website', ''),
            scraped_data.get('website', '')
        )
        results['comparisons']['website'] = {
            'status': website_result,
            'score': website_score,
            'original': original_data.get('Website', ''),
            'scraped': scraped_data.get('website', '')
        }
        
        # Add other scraped fields for reference
        results['scraped_address'] = scraped_data.get('address', '')
        results['scraped_specialty'] = scraped_data.get('specialty', '')
        results['has_photo'] = scraped_data.get('has_photo', False)
        
        # Calculate overall match score
        scores = [comp['score'] for comp in results['comparisons'].values() if comp['score'] > 0]
        results['overall_score'] = sum(scores) / len(scores) if scores else 0.0
        
        return results