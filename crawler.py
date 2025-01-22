from requests_tor import RequestsTor
from bs4 import BeautifulSoup
import re
import logging
from database.db_connect import *
from tqdm import tqdm
import urllib.parse
from multiprocessing import Pool, Manager
from functools import partial

# Setup logging with more detail
logger = logging.getLogger('scraper')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('scraper.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.propagate = False

def is_valid_onion(url):
    """Check if the URL is a valid .onion address."""
    if not url:
        return False
    pattern = r'(?:[a-z2-7]{16,56}\.onion)'
    return bool(re.search(pattern, url, re.IGNORECASE))

def normalize_onion_url(url):
    """Normalize the onion URL to ensure consistent format."""
    if not url:
        return None
    # Strip whitespace and remove any quotes
    url = url.strip().strip('"\'')
    
    # Add http:// if no protocol is present
    if not url.startswith(('http://', 'https://')):
        url = f'http://{url}'
    
    # Remove trailing slash
    url = url.rstrip('/')
    
    # Ensure it's a .onion URL
    if not is_valid_onion(url):
        return None
        
    return url

def extract_onion_links(soup, base_url):
    """Extract onion links from HTML content."""
    links = set()
    
    # Extract from href attributes
    for a in soup.find_all('a', href=True):
        href = a['href']
        try:
            # Handle relative URLs
            if href.startswith('/'):
                href = urllib.parse.urljoin(base_url, href)
            elif not href.startswith(('http://', 'https://')):
                href = urllib.parse.urljoin(base_url, href)
                
            if is_valid_onion(href):
                normalized = normalize_onion_url(href)
                if normalized:
                    links.add(normalized)
        except Exception as e:
            logger.error(f"Error processing href {href}: {e}")

    # Extract from text content using regex
    try:
        text = soup.get_text()
        pattern = r'(?:http:\/\/|https:\/\/)?(?:[a-zA-Z0-9-]+\.)*[a-z2-7]{16,56}\.onion(?:\/[^\s\'"<>()]*)?'
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            url = match.group(0)
            normalized = normalize_onion_url(url)
            if normalized:
                links.add(normalized)
    except Exception as e:
        logger.error(f"Error extracting links from text: {e}")

    logger.info(f"Found {len(links)} onion links in {base_url}")
    return links

def crawl_url(rt, url, visited_urls, depth=0, max_depth=2):
    """Recursively crawl a URL and its linked pages."""
    if depth > max_depth or url in visited_urls:
        return set()

    logger.info(f"Starting crawl of {url} at depth {depth}")
    visited_urls.append(url)
    discovered_links = set()

    try:
        response = rt.get(url, timeout=30)  # Increased timeout
        logger.info(f"Response from {url}: Status {response.status_code}")
        
        if response.status_code == 200:
            logger.info(f"UP - {url}")
            uplink_commit(url)
            
            soup = BeautifulSoup(response.text, "html.parser")
            new_links = extract_onion_links(soup, url)
            logger.info(f"Discovered {len(new_links)} new links from {url}")
            
            discovered_links.update(new_links)
            
            # Recursively crawl each new link
            for link in new_links:
                if link not in visited_urls:
                    logger.info(f"Recursively crawling {link}")
                    sub_links = crawl_url(rt, link, visited_urls, depth + 1, max_depth)
                    discovered_links.update(sub_links)
        else:
            logger.warning(f"DOWN - {url} (Status: {response.status_code})")
            downlink_commit(url)
    except Exception as e:
        logger.error(f"Error accessing {url}: {str(e)}")
        downlink_commit(url)
    
    return discovered_links

def process_base_url(args):
    """Process a single base URL and all its discovered links."""
    base_url, visited_urls = args
    rt = RequestsTor()
    logger.info(f"Starting to process base URL: {base_url}")
    
    discovered_links = crawl_url(rt, base_url, visited_urls)
    logger.info(f"Completed processing {base_url}. Found {len(discovered_links)} total links")
    
    return discovered_links

def main():
    database_create()
    create_table()
    max_workers = 2  # Reduced number of workers for better stability
    
    try:
        with open("base_list.txt", "r") as file:
            base_urls = set()
            for line in file:
                url = normalize_onion_url(line.strip())
                if url:
                    base_urls.add(url)
            
        if not base_urls:
            logger.warning("No valid base URLs found in the file.")
            return

        logger.info(f"Starting crawl with {len(base_urls)} base URLs")

        # Setup multiprocessing
        with Manager() as manager:
            visited_urls = manager.list()
            
            with Pool(processes=max_workers) as pool:
                results = pool.map(partial(process_base_url),
                                 [(url, visited_urls) for url in base_urls])
            
            all_discovered = set().union(*results) if results else set()
            
            logger.info(f"Crawl completed:")
            logger.info(f"Total unique links discovered: {len(all_discovered)}")
            logger.info(f"Total links processed: {len(visited_urls)}")

    except FileNotFoundError:
        logger.error("Base links file not found: base_list.txt")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()