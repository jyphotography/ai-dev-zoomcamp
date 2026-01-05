"""Test script for the web scraping tool"""

from main import scrape_web_impl

def test_scrape_web():
    """Test the scrape_web function with the minsearch repository"""
    url = "https://github.com/alexeygrigorev/minsearch"
    
    print(f"Scraping: {url}")
    print("=" * 50)
    
    content = scrape_web_impl(url)
    
    print(f"\nContent length: {len(content)} characters")
    print(f"\nFirst 500 characters:")
    print("-" * 50)
    print(content[:500])
    print("-" * 50)
    print(f"\nLast 500 characters:")
    print("-" * 50)
    print(content[-500:])
    
    return len(content)

if __name__ == "__main__":
    char_count = test_scrape_web()
    print(f"\nTotal characters: {char_count}")
