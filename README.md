# Tor Network Research Crawler

⚠️ **WARNING: DARK WEB RESEARCH SAFETY**

This tool is designed for legitimate research purposes only. Accessing the dark web can expose you to harmful, illegal, or disturbing content. Ensure you understand the risks and take appropriate safety precautions.

## ⚡ IMPORTANT DISCLAIMERS

1. **Legal Compliance**: This tool is intended for legitimate security research only. Users are responsible for complying with all applicable laws and regulations in their jurisdiction.

2. **Safety Precautions**:
   - Always use appropriate security measures (VPN, secure OS, etc.)
   - Never expose personal information
   - Use dedicated research devices when possible
   - Keep Tor and all security tools updated

3. **Usage Responsibility**:
   - The developers are not responsible for any misuse of this tool
   - No warranty is provided for the software
   - Users assume all risks associated with dark web research

4. **Content Warning**:
   - The dark web may contain disturbing or illegal content
   - This tool may encounter harmful material during crawling
   - Users should implement appropriate content filtering
   - Report illegal content to proper authorities

## Features

### Crawling Features
- Recursive crawling of .onion addresses with configurable depth
- Multi-process support for parallel crawling
- Robust URL validation and normalization
- PostgreSQL database integration for persistent storage
- Comprehensive logging system
- Hash-based duplicate detection

### Content Extraction Features
- Batch processing of discovered URLs
- Multi-threaded content scraping with Tor integration
- Intelligent main content extraction
- XML feed generation
- Content cleaning and normalization
- Configurable batch sizes

### Data Conversion Features
- XML to JSON conversion
- Structured data output
- Batch file processing
- Preserved data hierarchy

## Project Structure

```
DarIntelligence/
├── crawler.py           # Main crawler script
├── scraper.py          # Content extraction script
├── converter.py        # XML to JSON converter
├── database/
│   └── db_connect.py   # Database utilities
├── base_list.txt       # Initial URLs
└── output/             # XML and JSON output directory
```

## Prerequisites

- Python 3.7+
- Tor service running on your system
- PostgreSQL database server
- Kali Linux environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone DarIntelligence
cd DarIntelligence
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure PostgreSQL:
   - Ensure PostgreSQL service is running
   - Default credentials are set to:
     - User: kali
     - Password: kali
     - Port: 5432

## Safety Best Practices

### System Security
- Use a dedicated research environment
- Keep all software updated
- Use security-focused OS (like Kali Linux)
- Implement proper firewall rules

### Operational Security
- Never use personal information
- Maintain separate research profiles
- Document all research activities
- Follow organizational security policies

## Usage

### Crawling
```bash
python crawler.py
```

### Content Extraction
```bash
python scraper.py
```

### Data Conversion
```bash
python converter.py
```

## Data Formats

### XML Output Structure
```xml
<feed>
  <entry>
    <identifier>[UUID]</identifier>
    <hash>[SHA-256 hash]</hash>
    <url>[.onion URL]</url>
    <scraped_data>[Extracted content]</scraped_data>
  </entry>
</feed>
```

### JSON Output Structure
```json
{
  "feed": {
    "entry": [
      {
        "identifier": "[UUID]",
        "hash": "[SHA-256 hash]",
        "url": "[.onion URL]",
        "scraped_data": "[Extracted content]"
      }
    ]
  }
}
```

## Component Details

### Crawler (crawler.py)
- Discovers and validates .onion URLs
- Stores URLs in PostgreSQL database
- Manages crawling depth and parallel processing

### Scraper (scraper.py)
- Processes URLs in configurable batch sizes
- Extracts main content while removing noise
- Generates structured XML feeds
- Features parallel processing with multiple Tor sessions

### Converter (converter.py)
- Converts XML output to JSON format
- Preserves data structure and hierarchy
- Processes batch files
- Creates human-readable JSON output

## Database Structure

Two main tables in PostgreSQL:

### uplinks
- `id`: UUID primary key
- `link`: URL string (max 300 chars)
- `hash`: SHA-256 hash of the link (unique)

### downlinks
- Same structure as uplinks, stores inactive links

## Error Handling

The system implements comprehensive error handling for:
- Network timeouts and connection failures
- Invalid URLs and malformed content
- Database errors
- XML parsing errors
- File I/O operations

## Emergency Contacts

If you encounter illegal content or security threats:
- Local Law Enforcement: [Add appropriate contact]
- Cybercrime Reporting: [Add appropriate contact]
- Project Security Team: [Add appropriate contact]

## Legal Compliance
- Understand relevant laws and regulations
- Maintain research documentation
- Follow ethical research guidelines
- Obtain necessary permissions

## Contributing

Please follow standard contribution guidelines and maintain thorough documentation of any changes.

## Liability Disclaimer

THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Users must understand that dark web research carries inherent risks. The developers of this tool assume no responsibility for any damages, losses, or legal issues arising from the use or misuse of this software.

## License

MIT License
