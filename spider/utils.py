import pyperclip
from urllib.parse import urlparse
import aiohttp
import asyncio
from pathlib import Path


def read_xml_file(file_path):
    """
    Reads the content of an XML file from the specified file path.

    Args:
        file_path (str): The path to the XML file to be read.

    Returns:
        str or None: The content of the file as a string if successful, otherwise None.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Failed to read file: {e}")
        return None


def save_json_to_file(page_data, output_file):
    """
    Saves the provided page data to a specified output file in JSON format.

    Args:
        page_data (dict): The data to be saved.
        output_file (str): The path to the file where data will be saved.
    """
    if page_data:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(str(page_data))
        print(f"File saved to: {output_file}")


def get_default_output_file():
    """
    Provides the default output file path on the desktop.

    Returns:
        Path: A Path object pointing to a file called 'output.txt' on the desktop.
    """
    home = Path.home()
    desktop = home / 'Desktop'
    if not desktop.exists():
        print(f"Desktop path not found: {desktop}, using home directory.")
        desktop = home

    return desktop / "output.txt"


def fetch_urls_from_clipboard():
    """
    Fetches URLs from the clipboard and validates them.

    Returns:
        list: A list of valid URLs retrieved from the clipboard.
    """
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


def is_valid_http_link(link):
    """
    Checks if a given link is a valid HTTP/HTTPS link.

    Args:
        link (str): The link to be checked.

    Returns:
        bool: True if the link is an HTTP or HTTPS URL, otherwise False.
    """
    parsed_url = urlparse(link)
    return parsed_url.scheme in ['http', 'https']


async def fetch_status(session, url):
    """
    Asynchronously fetches the HTTP status code of a given URL.

    Args:
        session (aiohttp.ClientSession): An aiohttp session for making requests.
        url (str): The URL to check the status of.

    Returns:
        tuple: The URL and its status code, or None if the request failed.
    """
    try:
        async with session.head(url, timeout=10) as response:
            return url, response.status
    except:
        return url, None


async def check_link_status_async(links):
    """
    Asynchronously checks the HTTP status of a list of links.

    Args:
        links (list): A list of URLs to check.

    Returns:
        list: A list of URLs with non-200 status codes.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_status(session, link) for link in links]
        results = await asyncio.gather(*tasks)
    non_200_links = [url for url, status in results if status != 200 or status is None]
    return non_200_links


def validate_link_statuses(links, checked_links):
    """
    Validates the HTTP status of a list of links, ensuring that previously checked links are not rechecked.

    Args:
        links (list): A list of URLs to check.
        checked_links (dict): A dictionary of previously checked links and their statuses.

    Returns:
        list: A list of non-200 status links for the current page.
    """
    http_links = [link for link in links if is_valid_http_link(link)]
    unchecked_links = [link for link in http_links if link not in checked_links]

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
