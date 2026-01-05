from fastmcp import FastMCP
import requests

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

if __name__ == "__main__":
    mcp.run()