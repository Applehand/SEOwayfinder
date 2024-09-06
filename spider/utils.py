import requests
import json
import os
import pyperclip
from urllib.parse import urlparse


def get_response_text(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'http://google.com/'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch URL: {e}")
        return None


def read_sitemap_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Failed to read file: {e}")
        return None


def write_to_file(page_data, output_file):
    if page_data:
        with open(output_file, "w") as file:
            json.dump(page_data, file, indent=4, ensure_ascii=False)


def get_default_output_file():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    return os.path.join(desktop_path, "output.txt")


def handle_paste_from_clipboard():
    sitemap_urls = []
    clipboard_content = pyperclip.paste()
    urls = [url.strip() for url in clipboard_content.splitlines() if url.strip()]
    for url in urls:
        if urlparse(url).scheme in ['http', 'https']:
            sitemap_urls.append(url)
        else:
            print(f"Invalid URL from clipboard: {url}")
    if not sitemap_urls:
        print("No valid URLs found in clipboard.")
    return sitemap_urls

