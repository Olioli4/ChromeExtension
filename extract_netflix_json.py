#!/usr/bin/env python3
"""
Netflix JSON Data Extractor
Processes Netflix data internally via native messaging from browser extension
Works as a native messaging host to receive data from the browser extension
"""

import json
import re
import sys
import struct
from pathlib import Path

# NOTE: This script works internally with the browser extension via native messaging
# The extension captures the fully rendered page data and sends it to this script
# This script processes the data and can send it to LibreOffice Calc or save as files

def read_message():
    """
    Read a message from the browser extension via native messaging
    
    Returns:
        dict: Message from browser extension or None if error
    """
    try:
        # Read message length (4 bytes)
        raw_length = sys.stdin.buffer.read(4)
        if len(raw_length) == 0:
            return None
        
        message_length = struct.unpack('=I', raw_length)[0]
        
        # Read message content
        message = sys.stdin.buffer.read(message_length).decode('utf-8')
        return json.loads(message)
    except Exception as e:
        return {"error": f"Failed to read message: {str(e)}"}

def send_message(message):
    """
    Send a message back to the browser extension via native messaging
    
    Args:
        message (dict): Message to send to browser extension
    """
    try:
        encoded_content = json.dumps(message).encode('utf-8')
        encoded_length = struct.pack('=I', len(encoded_content))
        
        sys.stdout.buffer.write(encoded_length)
        sys.stdout.buffer.write(encoded_content)
        sys.stdout.buffer.flush()
    except Exception as e:
        # Send error back to extension
        error_msg = {"error": f"Failed to send message: {str(e)}"}
        encoded_content = json.dumps(error_msg).encode('utf-8')
        encoded_length = struct.pack('=I', len(encoded_content))
        sys.stdout.buffer.write(encoded_length)
        sys.stdout.buffer.write(encoded_content)
        sys.stdout.buffer.flush()

def extract_netflix_json_from_content(html_content):
    """
    Extract Netflix JSON-LD structured data from HTML content
    
    Args:
        html_content (str): HTML content string
        
    Returns:
        dict: Extracted Netflix data or None if not found
    """
    if not html_content:
        return None
    
    # Look for JSON-LD structured data with schema.org context
    json_pattern = r'\{"@context":"http://schema\.org".*?\}'
    
    matches = re.findall(json_pattern, html_content, re.DOTALL)
    
    if not matches:
        print("No JSON-LD structured data found in the HTML content")
        return None
    
    try:
        # Parse the first match (should be the main content)
        json_data = json.loads(matches[0])
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
        return None

def extract_netflix_json(html_file_path):
    """
    Extract Netflix JSON-LD structured data from HTML file
    
    Args:
        html_file_path (str): Path to the HTML file
        
    Returns:
        dict: Extracted Netflix data or None if not found
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    return extract_netflix_json_from_content(html_content)

def format_netflix_data(json_data):
    """
    Format Netflix data into a clean, readable structure
    
    Args:
        json_data (dict): Raw JSON data from Netflix
        
    Returns:
        dict: Formatted Netflix data
    """
    if not json_data:
        return None
    
    formatted_data = {
        "title": json_data.get("name", "Unknown"),
        "type": json_data.get("@type", "Unknown"),
        "url": json_data.get("url", ""),
        "netflix_id": "",
        "content_rating": json_data.get("contentRating", ""),
        "genre": json_data.get("genre", ""),
        "description": json_data.get("description", ""),
        "release_date": json_data.get("dateCreated", ""),
        "image_url": json_data.get("image", ""),
        "cast": [],
        "directors": [],
        "creators": []
    }
    
    # Extract Netflix ID from URL
    if formatted_data["url"]:
        id_match = re.search(r'/title/(\d+)', formatted_data["url"])
        if id_match:
            formatted_data["netflix_id"] = id_match.group(1)
    
    # Process cast
    actors = json_data.get("actors", [])
    for actor in actors:
        if isinstance(actor, dict) and actor.get("name"):
            formatted_data["cast"].append(actor["name"])
    
    # Process directors
    directors = json_data.get("director", [])
    for director in directors:
        if isinstance(director, dict) and director.get("name"):
            formatted_data["directors"].append(director["name"])
    
    # Process creators
    creators = json_data.get("creator", [])
    for creator in creators:
        if isinstance(creator, dict) and creator.get("name"):
            formatted_data["creators"].append(creator["name"])
    
    return formatted_data

def save_json_data(data, output_file):
    """
    Save formatted data to JSON file
    
    Args:
        data (dict): Data to save
        output_file (str): Output file path
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"Netflix data saved to: {output_file}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

def print_summary(data):
    """
    Print a summary of the extracted Netflix data
    
    Args:
        data (dict): Netflix data
    """
    if not data:
        print("No data to display")
        return
    
    print("\n" + "="*60)
    print("NETFLIX CONTENT SUMMARY")
    print("="*60)
    print(f"Title: {data['title']}")
    print(f"Type: {data['type']}")
    print(f"Netflix ID: {data['netflix_id']}")
    print(f"Content Rating: {data['content_rating']}")
    print(f"Genre: {data['genre']}")
    print(f"Release Date: {data['release_date']}")
    print(f"\nDescription:")
    print(f"  {data['description']}")
    
    if data['cast']:
        print(f"\nCast ({len(data['cast'])} actors):")
        for i, actor in enumerate(data['cast'], 1):
            print(f"  {i}. {actor}")
    
    if data['directors']:
        print(f"\nDirectors:")
        for director in data['directors']:
            print(f"  • {director}")
    
    if data['creators']:
        print(f"\nCreators:")
        for creator in data['creators']:
            print(f"  • {creator}")
    
    print(f"\nImage URL: {data['image_url']}")
    print(f"Netflix URL: {data['url']}")
    print("="*60)

def main():
    """
    Main function - works as native messaging host for browser extension
    Processes Netflix data received from the extension
    """
    try:
        # Check if running as native messaging host (no arguments)
        if len(sys.argv) == 1:
            # Native messaging mode - read from browser extension
            while True:
                message = read_message()
                if message is None:
                    break
                
                if "error" in message:
                    send_message({"error": message["error"]})
                    continue
                
                # Process the HTML content from the extension
                html_content = message.get("htmlContent", "")
                if not html_content:
                    send_message({"error": "No HTML content received"})
                    continue
                
                # Extract Netflix JSON data
                raw_json = extract_netflix_json_from_content(html_content)
                if not raw_json:
                    send_message({"error": "Failed to extract JSON data from HTML"})
                    continue
                
                # Format the data
                formatted_data = format_netflix_data(raw_json)
                if not formatted_data:
                    send_message({"error": "Failed to format data"})
                    continue
                
                # Save files if requested
                save_to_files = message.get("saveFiles", True)
                if save_to_files:
                    try:
                        output_dir = Path("d:/Browsertocalc")
                        output_dir.mkdir(parents=True, exist_ok=True)
                        
                        netflix_id = formatted_data.get('netflix_id', 'unknown')
                        
                        # Save formatted data
                        output_file = output_dir / f"netflix_extracted_data_{netflix_id}.json"
                        save_json_data(formatted_data, output_file)
                        
                        # Save raw JSON
                        raw_output_file = output_dir / f"netflix_raw_json_{netflix_id}.json"
                        save_json_data(raw_json, raw_output_file)
                        
                        formatted_data["savedFiles"] = {
                            "formatted": str(output_file),
                            "raw": str(raw_output_file)
                        }
                    except Exception as e:
                        formatted_data["fileError"] = f"Could not save files: {str(e)}"
                
                # Send response back to extension
                send_message({
                    "success": True,
                    "data": formatted_data,
                    "raw": raw_json
                })
        
        else:
            # Command line mode for testing - process HTML files
            import argparse
            
            parser = argparse.ArgumentParser(description='Extract Netflix JSON data from HTML files (testing mode)')
            parser.add_argument('input', nargs='?', help='Path to HTML file')
            parser.add_argument('--file', '-f', help='Path to HTML file to process')
            parser.add_argument('--output', '-o', help='Output directory for JSON files')
            
            args = parser.parse_args()
            
            # Determine input source
            input_source = None
            raw_json = None
            
            if args.file:
                input_source = args.file
                html_file = Path(args.file)
                if not html_file.exists():
                    print(f"Error: HTML file not found at {html_file}")
                    sys.exit(1)
                raw_json = extract_netflix_json(html_file)
            elif args.input:
                input_source = args.input
                html_file = Path(args.input)
                if not html_file.exists():
                    print(f"Error: HTML file not found at {html_file}")
                    sys.exit(1)
                raw_json = extract_netflix_json(html_file)
            else:
                # Default to existing files for testing
                html_files = [
                    Path("d:/Browsertocalc/netflix_raw_output.html"),
                    Path("d:/Browsertocalc/netflix_raw_response.html")
                ]
                
                for html_file in html_files:
                    if html_file.exists():
                        input_source = str(html_file)
                        print(f"Using default file: {html_file}")
                        raw_json = extract_netflix_json(html_file)
                        break
                else:
                    print("No input specified and no default HTML files found.")
                    print("Usage examples:")
                    print("  python extract_netflix_json.py --file netflix_page.html")
                    print("  python extract_netflix_json.py netflix_page.html")
                    print("\nNote: This script primarily works as a native messaging host.")
                    print("Command line mode is for testing only.")
                    sys.exit(1)
            
            if not raw_json:
                print("Failed to extract JSON data from HTML file")
                sys.exit(1)
            
            # Format and display data
            formatted_data = format_netflix_data(raw_json)
            if not formatted_data:
                print("Failed to format data")
                sys.exit(1)
            
            print_summary(formatted_data)
            
            # Save files in command line mode
            if args.output:
                output_dir = Path(args.output)
            else:
                output_dir = Path("d:/Browsertocalc")
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            netflix_id = formatted_data.get('netflix_id', 'unknown')
            output_file = output_dir / f"netflix_extracted_data_{netflix_id}.json"
            save_json_data(formatted_data, output_file)
            
            raw_output_file = output_dir / f"netflix_raw_json_{netflix_id}.json"
            save_json_data(raw_json, raw_output_file)
            print(f"Raw JSON data saved to: {raw_output_file}")
            
            print(f"\nInput source: {input_source}")
            print(f"Output directory: {output_dir}")
    
    except Exception as e:
        if len(sys.argv) == 1:
            # Native messaging mode - send error to extension
            send_message({"error": f"Script error: {str(e)}"})
        else:
            # Command line mode - print error
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
