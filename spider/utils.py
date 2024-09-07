import requests
import json
import pyperclip
from urllib.parse import urlparse
import aiohttp
import asyncio
from pathlib import Path


def read_xml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Failed to read file: {e}")
        return None


def save_json_to_file(page_data, output_file):
    if page_data:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(str(page_data))
        print(f"File saved to: {output_file}")


def get_default_output_file():
    home = Path.home()
    desktop = home / 'Desktop'
    if not desktop.exists():
        print(f"Desktop path not found: {desktop}, using home directory.")
        desktop = home

    return desktop / "output.txt"


def fetch_urls_from_clipboard():
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


def validate_link_statuses(links, checked_links):
    unchecked_links = [link for link in links if link not in checked_links]
    new_non_200_links = asyncio.run(check_link_status_async(unchecked_links))

    for link in unchecked_links:
        if link in new_non_200_links:
            checked_links[link] = "non-200"
        else:
            checked_links[link] = "200"

    non_200_links_for_current_page = [
        link for link in links if checked_links.get(link) == "non-200"
    ]

    return non_200_links_for_current_page


