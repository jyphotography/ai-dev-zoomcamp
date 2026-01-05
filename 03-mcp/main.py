from fastmcp import FastMCP
import requests
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def scrape_web_impl(url: str) -> str:
    """Scrape the content of a web page and return it as markdown.
    
    Uses Jina Reader to convert web pages to markdown format.
    Simply prepend 'r.jina.ai/' to any URL to get its markdown content.
    
    Args:
        url: The URL of the web page to scrape (e.g., 'https://datatalks.club')
    
    Returns:
        The markdown content of the web page
    """
    # Construct Jina Reader URL
    jina_url = f"https://r.jina.ai/{url}"
    
    try:
        # Disable SSL verification for testing (not recommended for production)
        response = requests.get(jina_url, timeout=30, verify=False)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error scraping {url}: {str(e)}"

@mcp.tool
def scrape_web(url: str) -> str:
    """Scrape the content of a web page and return it as markdown.
    
    Uses Jina Reader to convert web pages to markdown format.
    Simply prepend 'r.jina.ai/' to any URL to get its markdown content.
    
    Args:
        url: The URL of the web page to scrape (e.g., 'https://datatalks.club')
    
    Returns:
        The markdown content of the web page
    """
    return scrape_web_impl(url)

@mcp.tool
def count_word_in_text(text: str, word: str) -> int:
    """Count how many times a word appears in a text (case-insensitive).
    
    Useful for counting word occurrences in scraped web content.
    
    Args:
        text: The text to search in
        word: The word to count
    
    Returns:
        The number of times the word appears in the text
    """
    text_lower = text.lower()
    word_lower = word.lower()
    return text_lower.count(word_lower)

if __name__ == "__main__":
    mcp.run()Count how many times the word "data" appears on https://datatalks.club/
Use available MCP tools for that