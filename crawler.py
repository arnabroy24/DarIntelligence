from requests_tor import RequestsTor
from bs4 import BeautifulSoup
import re
import logging

# Setup logging
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def write_to_file(file_path, content):
    """Write unique content to a file."""
    try:
        with open(file_path, "a+") as file:
            file.seek(0)
            existing_content = set(file.read().splitlines())
            if content not in existing_content:
                file.write(content + "\n")
                logging.info(f"Added to file: {content}")
    except Exception as e:
        logging.error(f"Error writing to file {file_path}: {e}")

def scrape_and_check_links(rt, base_url, up_file, down_file):
    """Scrape onion links and check their status."""
    try:
        response = rt.get(base_url, timeout=15)
        if response.status_code == 200:
            logging.info(f"UP - {base_url}")
            write_to_file(up_file, base_url)
            soup = BeautifulSoup(response.text, "html.parser")
            links = set(re.findall(r'(?:http:\/\/)?[a-z2-7]{16,56}\.onion', soup.get_text()))
            for link in links:
                link = f"http://{link}" if not link.startswith("http://") else link
                check_and_log_status(rt, link, up_file, down_file)
        else:
            logging.warning(f"DOWN - {base_url}")
            write_to_file(down_file, base_url)
    except Exception as e:
        logging.error(f"Error processing {base_url}: {e}")
        write_to_file(down_file, base_url)

def check_and_log_status(rt, url, up_file, down_file):
    """Check the status of a URL and log the result."""
    try:
        response = rt.get(url, timeout=15)
        if response.status_code == 200:
            logging.info(f"UP - {url}")
            write_to_file(up_file, url)
        else:
            logging.warning(f"DOWN - {url}")
            write_to_file(down_file, url)
    except Exception as e:
        logging.error(f"Error accessing {url}: {e}")
        write_to_file(down_file, url)

def main():
    rt = RequestsTor()
    up_file = "uptime-links.txt"
    down_file = "downtime-links.txt"
    base_links_file = "base_lists.txt"

    try:
        with open(base_links_file, "r") as file:
            base_urls = [url.strip() for url in file if url.strip()]
            if not base_urls:
                logging.warning("No base URLs found in the file.")
                return
            for base_url in base_urls:
                logging.info(f"Processing Base URL: {base_url}")
                scrape_and_check_links(rt, base_url, up_file, down_file)
    except FileNotFoundError:
        logging.error(f"Base links file not found: {base_links_file}")
    except Exception as e:
        logging.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()