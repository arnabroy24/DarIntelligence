# Dark Web Onion Link Status Checker

This project is a Python-based script to scrape and check the status of onion links on the dark web. It uses `requests_tor` to route traffic through the Tor network, ensuring anonymity, and `BeautifulSoup` for parsing HTML content.

## Features
- Scrapes `.onion` links from a list of base URLs.
- Checks the status of the scraped links (up or down).
- Categorizes links into `uptime-links.txt` (active) and `downtime-links.txt` (inactive).
- Ensures anonymity using the Tor network.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/dark-web-link-checker.git
   cd dark-web-link-checker
   ```
2. Install dependencies:
```bash
pip install requests_tor beautifulsoup4
```
Ensure you have Tor installed and running on your system. Download Tor.

## Usage

```bash
python dark_web_checker.py
```
The script will scrape onion links from the specified base URLs and check their statuses. Results will be saved in the respective text files.

## Warning
⚠️ Caution while surfing dark web links:

These links are part of the dark web and may contain illegal or harmful content.
Ensure you have adequate security measures in place before accessing these links.
Always use Tor Browser or a secure Tor-enabled connection for accessing .onion links.

### Disclaimer
This project is intended for educational and research purposes only. The author does not promote or condone any illegal activity. Use this tool responsibly.
