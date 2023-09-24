from bs4 import BeautifulSoup
import requests
from .models import Card
import logging
import re

logger = logging.getLogger(__name__)

def scrape_history_data(title, url):
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for element in soup.find_all('div', class_=['quotebox', 'thumbinner multiimageinner']):
            element.decompose()

        
        for style_tag in soup.find_all('style'):
            style_tag.decompose()
        
        
        for figcaption in soup.find_all('figcaption'):
            figcaption.decompose()
        
        # Compile a regular expression pattern for case insensitive search
        title_pattern = re.compile(re.escape(' '.join(title.split())), re.IGNORECASE)
        
        # Find all sections with headers (h1, h2, etc.)
        events = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        data = []
        for event in events:
            if title_pattern.search(' '.join(event.get_text().split())):
                section_text = event.get_text().lower()
                
                # Skip unwanted sections
                if any(unwanted_section in section_text for unwanted_section in ["bibliography", "citations", "explanatory notes", "references", "contents"]):
                    continue
                
                section_content = []
                for sibling in event.find_next_siblings():
                    if sibling.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        break  # Stop the loop when encountering another heading
                    if "Main articles:" not in sibling.get_text() and "Main article:" not in sibling.get_text() and "Further information:" not in sibling.get_text() and "See also:" not in sibling.get_text():
                        section_content.append(sibling)
                
                section_text = "\n".join([
                    re.sub(r'\[.*?\]', '', content.get_text()) 
                    for content in section_content 
                    if content.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
                ])

                data.append({
                    "title": event.get_text(),
                    "content": section_text
                })

        return data

    else:
        logging.error(f"Failed to retrieve data from {url}. HTTP Status Code: {response.status_code}")
        return None



def save_history_data(data, title, source_url):
    if data:
        seen_titles = set()
        for item in data:
            # Clean the title by removing "(edit)"
            clean_title = item["title"].replace("[edit]", "").strip()

            if clean_title not in seen_titles:
                # Check if a record with similar attributes already exists
                existing_records = Card.objects.filter(title__icontains=clean_title, source_url=source_url)
                if existing_records.exists():
                    # If existing records are found, update the first record with the new content and increment the update count
                    existing_record = existing_records.first()
                    update_count = existing_record.description.count('Update')
                    new_update_count = update_count + 1
                    new_description = f"{item['content']} (Update {new_update_count})"
                    existing_record.description = new_description
                    existing_record.save()
                else:
                    # If no existing record is found, create a new record
                    Card.objects.create(
                        title=clean_title,
                        description=item["content"],
                        source_url=source_url
                    )
                seen_titles.add(clean_title)
    else:
        logger.error(f"No data found : {data}")








def validate_input(input_str):
    if not input_str or not isinstance(input_str, str):
        return None, "Invalid input. Please provide a valid input as a non-empty string."
    else:
        return input_str, None


