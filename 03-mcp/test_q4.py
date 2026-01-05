"""Test script for Question 4: Count word occurrences using the web scraping tool"""

from main import scrape_web_impl

def count_word_occurrences(text: str, word: str) -> int:
    """Count how many times a word appears in text (case-insensitive)"""
    text_lower = text.lower()
    word_lower = word.lower()
    return text_lower.count(word_lower)

def test_count_data():
    """Test counting the word 'data' on datatalks.club"""
    url = "https://datatalks.club/"
    
    print(f"Scraping: {url}")
    print("=" * 50)
    
    # Scrape the content
    content = scrape_web_impl(url)
    
    if content.startswith("Error"):
        print(f"Error occurred: {content}")
        return None
    
    # Count occurrences of "data"
    count = count_word_occurrences(content, "data")
    
    print(f"\nContent length: {len(content)} characters")
    print(f"Number of times 'data' appears: {count}")
    
    # Show some context around occurrences
    print("\n" + "=" * 50)
    print("Sample occurrences (first 5):")
    print("-" * 50)
    
    content_lower = content.lower()
    word = "data"
    index = 0
    found = 0
    
    while found < 5 and index < len(content_lower):
        pos = content_lower.find(word, index)
        if pos == -1:
            break
        
        # Show context (50 chars before and after)
        start = max(0, pos - 50)
        end = min(len(content), pos + len(word) + 50)
        context = content[start:end].replace('\n', ' ')
        print(f"  ...{context}...")
        
        index = pos + 1
        found += 1
    
    return count

if __name__ == "__main__":
    count = test_count_data()
    if count is not None:
        print(f"\n{'='*50}")
        print(f"Final answer: {count} occurrences of 'data'")
        print(f"\nClosest match options:")
        print(f"  61, 111, 161, 261")
