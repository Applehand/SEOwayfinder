from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


def fetch_sitemap_content(sitemap_url):
    try:
        html = fetch_url_content(sitemap_url)
        if not html:
            return None, sitemap_url

        soup_obj = BeautifulSoup(html, "html.parser")
        parsed_url = urlparse(sitemap_url)

        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        print(f"Crawling URL: {base_url}")

        return soup_obj, base_url

    except Exception as e:
        print(f"Error crawling URL {sitemap_url}: {e}")
        return None, sitemap_url


def fetch_url_content(url):
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