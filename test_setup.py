#!/usr/bin/env python3
"""
Test script to verify the Doctor Directory Audit Tool setup
"""

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ Pandas imported successfully")
    except ImportError as e:
        print(f"✗ Pandas import failed: {e}")
        return False
    
    try:
        import selenium
        print("✓ Selenium imported successfully")
    except ImportError as e:
        print(f"✗ Selenium import failed: {e}")
        return False
    
    try:
        from utils.search_engine import SearchEngine
        print("✓ SearchEngine imported successfully")
    except ImportError as e:
        print(f"✗ SearchEngine import failed: {e}")
        return False
    
    try:
        from utils.comparison import ProfileComparator
        print("✓ ProfileComparator imported successfully")
    except ImportError as e:
        print(f"✗ ProfileComparator import failed: {e}")
        return False
    
    try:
        from scrapers.scraper_factory import ScraperFactory
        print("✓ ScraperFactory imported successfully")
    except ImportError as e:
        print(f"✗ ScraperFactory import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of key components"""
    print("\nTesting basic functionality...")
    
    try:
        from utils.search_engine import SearchEngine
        search_engine = SearchEngine()
        print("✓ SearchEngine instance created")
    except Exception as e:
        print(f"✗ SearchEngine creation failed: {e}")
        return False
    
    try:
        from utils.comparison import ProfileComparator
        comparator = ProfileComparator()
        print("✓ ProfileComparator instance created")
    except Exception as e:
        print(f"✗ ProfileComparator creation failed: {e}")
        return False
    
    try:
        from scrapers.scraper_factory import ScraperFactory
        scraper = ScraperFactory.get_scraper("vitals.com")
        print("✓ VitalsScraper instance created")
    except Exception as e:
        print(f"✗ VitalsScraper creation failed: {e}")
        return False
    
    try:
        # Test comparison functionality
        test_data1 = {"name": "Dr. John Smith", "phone": "123-456-7890"}
        test_data2 = {"name": "John Smith, MD", "phone": "123-456-7890"}
        
        comparison = comparator.compare_profiles(test_data1, test_data2)
        print("✓ Profile comparison working")
    except Exception as e:
        print(f"✗ Profile comparison failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from config import DEFAULT_DIRECTORIES, MAX_SEARCH_RESULTS
        print(f"✓ Default directories loaded: {DEFAULT_DIRECTORIES}")
        print(f"✓ Max search results: {MAX_SEARCH_RESULTS}")
    except ImportError as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("Doctor Directory Audit Tool - Setup Test")
    print("=" * 50)
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
    
    if not test_basic_functionality():
        all_passed = False
        
    if not test_config():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Setup is complete.")
        print("\nYou can now run the application with:")
        print("  ./run_app.sh")
        print("  or")
        print("  streamlit run main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    main()