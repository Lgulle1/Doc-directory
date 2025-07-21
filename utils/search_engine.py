from googlesearch import search
import time
import logging
from urllib.parse import urlparse

class SearchEngine:
    """Handle Google searches for doctor profiles"""
    
    def __init__(self, max_results=3, delay=1):
        self.max_results = max_results
        self.delay = delay
        self.logger = logging.getLogger(__name__)
    
    def search_doctor_on_domain(self, doctor_name, location, domain):
        """
        Search for a doctor on a specific domain
        Returns list of URLs found
        """
        try:
            # Construct search query
            query = f'site:{domain} "{doctor_name}" {location}'
            self.logger.info(f"Searching: {query}")
            
            # Perform search
            search_results = []
            for url in search(query, num_results=self.max_results, sleep_interval=self.delay):
                search_results.append(url)
                if len(search_results) >= self.max_results:
                    break
            
            # Filter results to ensure they're from the correct domain
            filtered_results = []
            for url in search_results:
                parsed_url = urlparse(url)
                if domain.lower() in parsed_url.netloc.lower():
                    filtered_results.append(url)
            
            self.logger.info(f"Found {len(filtered_results)} results for {doctor_name} on {domain}")
            return filtered_results
            
        except Exception as e:
            self.logger.error(f"Search error for {doctor_name} on {domain}: {str(e)}")
            return []
    
    def search_doctor_all_domains(self, doctor_name, location, domains):
        """
        Search for a doctor across multiple domains
        Returns dict with domain as key and list of URLs as value
        """
        all_results = {}
        
        for domain in domains:
            self.logger.info(f"Searching {domain} for {doctor_name}")
            urls = self.search_doctor_on_domain(doctor_name, location, domain)
            all_results[domain] = urls
            
            # Be respectful with search requests
            time.sleep(self.delay)
        
        return all_results