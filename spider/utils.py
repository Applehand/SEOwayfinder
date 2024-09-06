import requests
import json
import os
import pyperclip
from urllib.parse import urlparse
import aiohttp
import asyncio
from pathlib import Path


def get_response_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
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
        print(f"File saved to: {output_file}")


def get_default_output_file():
    home = Path.home()
    desktop = home / 'Desktop'
    if not desktop.exists():
        print(f"Desktop path not found: {desktop}, using home directory.")
        desktop = home

    return desktop / "output.txt"


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


async def fetch_status(session, url):
    try:
        async with session.head(url, timeout=10) as response:
            return url, response.status
    except:
        return url, None


async def check_link_status_async(links):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_status(session, link) for link in links]
        results = await asyncio.gather(*tasks)
    non_200_links = [url for url, status in results if status != 200 or status is None]
    return non_200_links


def check_link_status(links):
    return asyncio.run(check_link_status_async(links))

