from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


def fetch_sitemap_content(sitemap_url):
    """
    Fetch and parse the content of a sitemap URL.

    Depending on the content type (XML or HTML), this function will use the appropriate
    parser (XML for sitemaps, HTML for individual web pages) to process the URL content.

    Args:
        sitemap_url (str): The URL of the sitemap or page to fetch and parse.

    Returns:
        bs4.BeautifulSoup: A BeautifulSoup object representing the parsed content, and the base URL (str).
        If the content could not be fetched, returns (None, sitemap_url).
    """
    try:
        html = fetch_url_content(sitemap_url)
        if not html:
            print(f"Failed to fetch or empty content for: {sitemap_url}")
            return None, sitemap_url

        if is_xml_content(html, sitemap_url):
            soup_obj = BeautifulSoup(html, "xml")
        else:
            soup_obj = BeautifulSoup(html, "html.parser")

        parsed_url = urlparse(sitemap_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        print(f"Successfully crawled URL: {base_url}")
        return soup_obj, base_url

    except Exception as e:
        print(f"Error crawling URL {sitemap_url}: {e}")
        return None, sitemap_url


def is_xml_content(content, url):
    """
    Determine whether the fetched content is XML or HTML.

    This function checks if the URL or content indicates XML format.

    Args:
        content (str): The raw content fetched from the URL.
        url (str): The URL from which the content was fetched.

    Returns:
        bool: True if the content is XML, otherwise False.
    """
    if url.endswith('.xml'):
        return True

    if content.lstrip().startswith('<?xml') or content.lstrip().startswith('<sitemapindex'):
        return True

    return False


def fetch_url_content(url):
    """
    Fetch the raw content of a URL.

    This function makes an HTTP GET request to the given URL and retrieves the content.
    If the request fails, it will return None.

    Args:
        url (str): The URL to fetch the content from.

    Returns:
        str: The raw content of the URL as a string. If fetching fails, returns None.
    """
    try:
        print(f"Making request to: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'http://google.com/'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        print(f"Successfully fetched content for: {url}")
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch URL: {e}")
        return None
