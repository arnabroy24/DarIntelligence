from requests_tor import RequestsTor
from bs4 import BeautifulSoup
import logging
import psycopg2
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from database.db_connect import *
from concurrent.futures import ThreadPoolExecutor
from functools import partial

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', ''.join(char for char in text if char.isprintable())).strip()

def extract_main_content(soup):
    for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'noscript']):
        element.decompose()
    
    main_content = soup.select_one('main, article, div.content, body')
    return clean_text(main_content.get_text()) if main_content else ""

def create_xml_feed(data, batch_num):
    root = ET.Element("feed")
    
    for item in data:
        entry = ET.SubElement(root, "entry")
        ET.SubElement(entry, "identifier").text = str(item['identifier'])
        ET.SubElement(entry, "hash").text = item['hash']
        ET.SubElement(entry, "url").text = item['url']
        ET.SubElement(entry, "scraped_data").text = item['content']
    
    return minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")

def process_url(row, rt):
    try:
        response = rt.get(row[1].strip())  # row[1] is the 'link' column
        soup = BeautifulSoup(response.text, "html.parser")
        content = extract_main_content(soup)
        
        if len(content) > 20:
            int_data = {
                'identifier': row[0],  # row[0] is the 'id' column
                'url': row[1],        # row[1] is the 'link' column
                'hash': row[2],       # row[2] is the 'hash' column
                'content': content
            }
            print(f"Successfully processed {row[1]}")
        else:
            int_data = {
                'identifier': row[0],
                'url': row[1],
                'hash': row[2],
                'content': "Insufficient content"
            }
            print(f"Skipped {row[1]} - insufficient content")
            
        return int_data
            
    except Exception as e:
        logging.error(f"Error processing URL {row[1]}: {str(e)}")
        return {
            'identifier': row[0],
            'url': row[1],
            'hash': row[2],
            'content': f"ERROR: {str(e)}"
        }

def scrape_websites_batch(start_index, batch_size):
    data = []
    
    try:
        # Database connection
        conn = psycopg2.connect(
            database="intelligence",
            user='kali',
            password='kali',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        
        # Fetch batch of URLs using correct column names
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, link, hash FROM uplinks 
                ORDER BY id
                OFFSET %s 
                LIMIT %s
            """, (start_index, batch_size))
            rows = cursor.fetchall()
        
        if not rows:
            print(f"No more rows to process starting from index {start_index}")
            return False
            
        # Initialize Tor sessions for parallel processing
        tor_sessions = [RequestsTor() for _ in range(3)]
        
        def get_tor_session(index):
            return tor_sessions[index % len(tor_sessions)]
        
        # Process URLs in parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for i, row in enumerate(rows):
                rt = get_tor_session(i)
                futures.append(
                    executor.submit(process_url, row, rt)
                )
            
            # Collect results
            for future in futures:
                try:
                    result = future.result()
                    if result:
                        data.append(result)
                except Exception as e:
                    logging.error(f"Thread execution failed: {str(e)}")
        
        # Create XML and save to file
        batch_num = 2
        xml_content = create_xml_feed(data, batch_num)
        output_path = f"/home/kali/Desktop/DarIntelligence/dark-web-info-batch-{batch_num}.xml"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"\nBatch {batch_num} data saved to {output_path}")
        
        # Preview first entry
        preview_root = ET.fromstring(xml_content)
        first_entry = preview_root.find('entry')
        if first_entry is not None:
            preview_xml = minidom.parseString(ET.tostring(first_entry)).toprettyxml(indent="  ")
            print(f"\nPreview of the first entry in batch {batch_num}:")
            print(preview_xml)
        
        return True
        
    except Exception as e:
        logging.error(f"Database or general error: {str(e)}")
        raise
    
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    try:
        batch_size = 200  # Number of links to process in each batch
        start_index = 200   # Starting index for the current batch
        
        while True:
            print(f"\nProcessing batch starting at index {start_index}")
            has_more_rows = scrape_websites_batch(start_index, batch_size)
            
            if not has_more_rows:
                print("All links have been processed!")
                break
                
            start_index += batch_size
            
    except Exception as e:
        logging.error(f"Script failed: {str(e)}")