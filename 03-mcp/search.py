"""Search implementation for Question 5: Index and search fastmcp documentation"""

import os
import zipfile
import urllib.request
from pathlib import Path
from minsearch import Index

# URL to download
ZIP_URL = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
ZIP_FILENAME = "fastmcp-main.zip"
EXTRACT_DIR = "fastmcp-main"


def download_zip(url: str, filename: str) -> bool:
    """Download zip file if it doesn't already exist."""
    if os.path.exists(filename):
        print(f"Zip file {filename} already exists, skipping download.")
        return False
    
    print(f"Downloading {url}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Downloaded {filename} successfully.")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        raise


def extract_zip(zip_filename: str, extract_dir: str):
    """Extract zip file."""
    if os.path.exists(extract_dir):
        print(f"Extract directory {extract_dir} already exists, skipping extraction.")
        return
    
    print(f"Extracting {zip_filename}...")
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall('.')
    print(f"Extracted to {extract_dir}")


def process_files(root_dir: str) -> list[dict]:
    """
    Process all .md and .mdx files in the directory.
    Returns a list of documents with 'content' and 'filename' fields.
    """
    documents = []
    root_path = Path(root_dir)
    
    # Find all .md and .mdx files
    md_files = list(root_path.rglob("*.md")) + list(root_path.rglob("*.mdx"))
    
    print(f"Found {len(md_files)} markdown files")
    
    for file_path in md_files:
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get relative path from root_dir
            relative_path = file_path.relative_to(root_path)
            
            # Convert to string and use forward slashes (for consistency)
            filename = str(relative_path).replace('\\', '/')
            
            # Create document
            doc = {
                'content': content,
                'filename': filename
            }
            documents.append(doc)
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
    
    print(f"Processed {len(documents)} documents")
    return documents


def build_index(documents: list[dict]) -> Index:
    """
    Build minsearch index with 'content' as text field and 'filename' as keyword field.
    """
    print("Building search index...")
    
    # Create index with 'content' as text field (for full-text search)
    # and 'filename' as keyword field (for exact matching/filtering)
    index = Index(
        text_fields=['content'],
        keyword_fields=['filename']
    )
    
    # Fit the index with documents
    index.fit(documents)
    
    print(f"Index built with {len(documents)} documents")
    return index


def search_docs(index: Index, query: str, num_results: int = 5) -> list[dict]:
    """
    Search the index and return top N most relevant documents.
    
    Args:
        index: The minsearch Index instance
        query: Search query string
        num_results: Number of results to return (default: 5)
    
    Returns:
        List of documents matching the query, ranked by relevance
    """
    results = index.search(query, num_results=num_results)
    return results


def main():
    """Main function to download, process, index, and test search."""
    print("=" * 70)
    print("Question 5: Search Implementation")
    print("=" * 70)
    
    # Step 1: Download zip file (if not already downloaded)
    download_zip(ZIP_URL, ZIP_FILENAME)
    
    # Step 2: Extract zip file
    extract_zip(ZIP_FILENAME, EXTRACT_DIR)
    
    # Step 3: Process files
    documents = process_files(EXTRACT_DIR)
    
    if not documents:
        print("No documents found to index!")
        return
    
    # Step 4: Build index
    index = build_index(documents)
    
    # Step 5: Test search with "demo" query
    print("\n" + "=" * 70)
    print("Testing search with query: 'demo'")
    print("=" * 70)
    
    results = search_docs(index, "demo", num_results=5)
    
    print(f"\nFound {len(results)} results:\n")
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc['filename']}")
        # Show preview of content
        content_preview = doc['content'][:200].replace('\n', ' ')
        print(f"   Preview: {content_preview}...")
        print()
    
    # Answer the question
    if results:
        first_file = results[0]['filename']
        print("=" * 70)
        print(f"First file returned for query 'demo': {first_file}")
        print("=" * 70)
        
        # Check which option it matches
        options = [
            "README.md",
            "docs/servers/context.mdx",
            "examples/testing_demo/README.md",
            "docs/python-sdk/fastmcp-settings.mdx"
        ]
        
        print("\nMatching options:")
        for opt in options:
            if opt in first_file or first_file.endswith(opt):
                print(f"  ✓ Matches: {opt}")
    else:
        print("No results found!")


if __name__ == "__main__":
    main()
