# example.py
# Simple script to prompt for a URL, fetch the content, and print the raw HTTP response or parsed content.

import requests

if __name__ == "__main__":
    url = input("Enter a URL to fetch: ")
    try:
        response = requests.get(url)
        print("Status:", response.status_code)
        print("Headers:", response.headers)
        print("\n--- Content (truncated to 1000 chars) ---\n")
        print(response.text[:1000])
    except Exception as e:
        print("Error fetching URL:", e)
