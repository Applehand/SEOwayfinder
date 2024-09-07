from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


def fetch_sitemap_content(sitemap_url):
    try:
        html = fetch_url_content(sitemap_url)
        if not html:
            print(f"Failed to fetch or empty content for: {sitemap_url}")
            return None, sitemap_url

        # Check if XML or HTML content and parse accordingly
        if is_xml_content(html, sitemap_url):
            print(f"Detected XML content for URL: {sitemap_url}")
            soup_obj = BeautifulSoup(html, "xml")
        else:
            print(f"Detected HTML content for URL: {sitemap_url}")
            soup_obj = BeautifulSoup(html, "html.parser")

        parsed_url = urlparse(sitemap_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        print(f"Successfully crawled URL: {base_url}")
        return soup_obj, base_url

    except Exception as e:
        print(f"Error crawling URL {sitemap_url}: {e}")
        return None, sitemap_url


def is_xml_content(content, url):
    if url.endswith('.xml'):
        return True

    if content.lstrip().startswith('<?xml') or content.lstrip().startswith('<sitemapindex'):
        return True

    return False


def fetch_url_content(url):
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
