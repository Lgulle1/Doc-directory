import streamlit as st
import pandas as pd
import logging
from io import StringIO
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import DEFAULT_DIRECTORIES, MAX_SEARCH_RESULTS
from utils.search_engine import SearchEngine
from utils.comparison import ProfileComparator
from scrapers.scraper_factory import ScraperFactory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_session_state():
    """Initialize session state variables"""
    if 'audit_results' not in st.session_state:
        st.session_state.audit_results = []
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False

def validate_csv_columns(df):
    """Validate that CSV has required columns"""
    required_columns = ['Name', 'Location', 'Website']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        st.info("Required columns: Name, Location, Website")
        return False
    return True

def process_doctor_profile(doctor_data, domains, search_engine, comparator):
    """Process a single doctor's profile across all domains"""
    doctor_name = doctor_data['Name']
    location = doctor_data['Location']
    
    logger.info(f"Processing {doctor_name} in {location}")
    
    # Search across all domains
    search_results = search_engine.search_doctor_all_domains(doctor_name, location, domains)
    
    profile_results = []
    
    # Process each domain's results
    for domain, urls in search_results.items():
        if not urls:
            # No results found for this domain
            profile_results.append({
                'doctor_name': doctor_name,
                'original_location': location,
                'original_website': doctor_data.get('Website', ''),
                'directory': domain,
                'profile_url': 'No results found',
                'comparisons': {},
                'scraped_address': '',
                'scraped_specialty': '',
                'has_photo': False,
                'overall_score': 0.0,
                'error': 'No search results found'
            })
            continue
        
        # Scrape each URL found
        scraper = ScraperFactory.get_scraper(domain)
        
        for url in urls:
            try:
                logger.info(f"Scraping {url}")
                scraped_data = scraper.extract_profile_data(url)
                
                # Compare with original data
                comparison_result = comparator.compare_profiles(doctor_data, scraped_data)
                
                profile_results.append(comparison_result)
                
            except Exception as e:
                logger.error(f"Error processing {url}: {str(e)}")
                profile_results.append({
                    'doctor_name': doctor_name,
                    'original_location': location,
                    'original_website': doctor_data.get('Website', ''),
                    'directory': domain,
                    'profile_url': url,
                    'comparisons': {},
                    'scraped_address': '',
                    'scraped_specialty': '',
                    'has_photo': False,
                    'overall_score': 0.0,
                    'error': str(e)
                })
        
        # Clean up scraper
        scraper.teardown_driver()
    
    return profile_results

def create_results_dataframe(results):
    """Convert results to a pandas DataFrame for display"""
    rows = []
    
    for result in results:
        row = {
            'Doctor Name': result['doctor_name'],
            'Directory': result['directory'],
            'Profile URL': result['profile_url'],
            'Overall Score': f"{result['overall_score']:.2f}",
            'Scraped Name': result['comparisons'].get('name', {}).get('scraped', ''),
            'Name Match': result['comparisons'].get('name', {}).get('status', ''),
            'Scraped Phone': result['comparisons'].get('phone', {}).get('scraped', '') if 'phone' in result['comparisons'] else '',
            'Phone Match': result['comparisons'].get('phone', {}).get('status', '') if 'phone' in result['comparisons'] else '',
            'Scraped Website': result['comparisons'].get('website', {}).get('scraped', ''),
            'Website Match': result['comparisons'].get('website', {}).get('status', ''),
            'Address': result['scraped_address'],
            'Specialty': result['scraped_specialty'],
            'Has Photo': result['has_photo'],
            'Error': result.get('error', '')
        }
        rows.append(row)
    
    return pd.DataFrame(rows)

def main():
    st.set_page_config(
        page_title="Doctor Directory Audit Tool",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("🏥 Doctor Directory Audit Tool")
    st.markdown("Upload a CSV with doctor information to audit their presence across medical directories.")
    
    init_session_state()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Default directories
        st.subheader("Default Directories")
        for domain in DEFAULT_DIRECTORIES:
            st.text(f"✓ {domain}")
        
        # Additional directories input
        st.subheader("Additional Directories")
        additional_domains = st.text_input(
            "Enter additional domains (comma-separated)",
            placeholder="zocdoc.com,md.com,caredash.com",
            help="Add custom medical directory domains to search"
        )
        
        # Parse additional domains
        custom_domains = []
        if additional_domains:
            custom_domains = [domain.strip() for domain in additional_domains.split(',') if domain.strip()]
        
        all_domains = DEFAULT_DIRECTORIES + custom_domains
        
        st.subheader("All Domains to Search")
        for domain in all_domains:
            st.text(f"• {domain}")
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Upload CSV File")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="CSV should contain columns: Name, Location, Website"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"Loaded {len(df)} doctor records")
                
                # Validate CSV structure
                if validate_csv_columns(df):
                    st.dataframe(df.head())
                    
                    # Process button
                    if st.button("Start Audit", type="primary"):
                        if len(df) > 10:
                            st.warning("Processing more than 10 doctors may take a while. Consider testing with a smaller sample first.")
                        
                        # Start processing
                        with st.spinner("Processing doctor profiles..."):
                            search_engine = SearchEngine(max_results=MAX_SEARCH_RESULTS)
                            comparator = ProfileComparator()
                            
                            all_results = []
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            # Process each doctor
                            for idx, (_, doctor_data) in enumerate(df.iterrows()):
                                status_text.text(f"Processing {doctor_data['Name']} ({idx + 1}/{len(df)})")
                                
                                try:
                                    doctor_results = process_doctor_profile(
                                        doctor_data, all_domains, search_engine, comparator
                                    )
                                    all_results.extend(doctor_results)
                                except Exception as e:
                                    logger.error(f"Error processing {doctor_data['Name']}: {str(e)}")
                                    st.error(f"Error processing {doctor_data['Name']}: {str(e)}")
                                
                                # Update progress
                                progress_bar.progress((idx + 1) / len(df))
                            
                            st.session_state.audit_results = all_results
                            st.session_state.processing_complete = True
                            status_text.text("Processing complete!")
                            
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")
    
    with col2:
        st.header("Audit Results")
        
        if st.session_state.processing_complete and st.session_state.audit_results:
            results_df = create_results_dataframe(st.session_state.audit_results)
            
            # Display summary metrics
            col2a, col2b, col2c = st.columns(3)
            
            with col2a:
                total_profiles = len(results_df)
                st.metric("Total Profiles Found", total_profiles)
            
            with col2b:
                matches = len(results_df[results_df['Name Match'] == 'Match'])
                st.metric("Name Matches", matches)
            
            with col2c:
                avg_score = results_df['Overall Score'].astype(float).mean()
                st.metric("Average Match Score", f"{avg_score:.2f}")
            
            # Display results table
            st.subheader("Detailed Results")
            
            # Add filters
            col_filter1, col_filter2 = st.columns(2)
            
            with col_filter1:
                directory_filter = st.selectbox(
                    "Filter by Directory",
                    ["All"] + list(results_df['Directory'].unique())
                )
            
            with col_filter2:
                match_filter = st.selectbox(
                    "Filter by Name Match Status",
                    ["All", "Match", "Mismatch", "Missing"]
                )
            
            # Apply filters
            filtered_df = results_df.copy()
            
            if directory_filter != "All":
                filtered_df = filtered_df[filtered_df['Directory'] == directory_filter]
            
            if match_filter != "All":
                filtered_df = filtered_df[filtered_df['Name Match'] == match_filter]
            
            # Display filtered results
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Download button
            csv_buffer = StringIO()
            results_df.to_csv(csv_buffer, index=False)
            
            st.download_button(
                label="Download Full Results as CSV",
                data=csv_buffer.getvalue(),
                file_name=f"doctor_audit_results_{int(time.time())}.csv",
                mime="text/csv"
            )
            
        elif st.session_state.processing_complete:
            st.info("No results to display. Upload a CSV file and click 'Start Audit' to begin.")
        else:
            st.info("Upload a CSV file and click 'Start Audit' to see results here.")

if __name__ == "__main__":
    main()