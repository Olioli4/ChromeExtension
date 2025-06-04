# example.py
# Simple script to prompt for a URL, fetch the content, and print the raw HTTP response or parsed content.

import requests
import re

def parse_netflix_url(url):
    """
    Fetch the given URL and return (name, image) if found, else (None, None).
    """
    try:
        response = requests.get(url, headers={'User-Agent': 'Python Example Script'})
        lines = response.text.split('\n')
        name_value = None
        image_value = None
        for line in lines:
            if name_value is None and '"name"' in line:
                match = re.search(r'"name"\s*:\s*"([^"\r\n]+)"', line)
                if match:
                    name_value = match.group(1)
            if image_value is None and '"image"' in line:
                match = re.search(r'"image"\s*:\s*"([^"\r\n]+)"', line)
                if match:
                    image_value = match.group(1)
            if name_value is not None and image_value is not None:
                break
        return name_value, image_value
    except Exception as e:
        print("Error fetching URL:", e)
        return None, None

if __name__ == "__main__":
    url = input("Enter a URL to fetch: ")
    name, image = parse_netflix_url(url)
    
    print("Name:", name)
    print("Image:", image)
