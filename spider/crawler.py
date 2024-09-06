from urllib.parse import urlparse
from bs4 import BeautifulSoup
from .utils import get_response_text


def crawl_sitemap_url(sitemap_url):
    try:
        html = get_response_text(sitemap_url)
        if not html:
            return None, sitemap_url  # Return None and the URL if fetching fails

        soup_obj = BeautifulSoup(html, "html.parser")
        parsed_url = urlparse(sitemap_url)

        # Construct the base URL with scheme, hostname, and path
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        print(f"Crawling URL: {base_url}")

        return soup_obj, base_url  # Return both soup object and base URL

    except Exception as e:
        print(f"Error crawling URL {sitemap_url}: {e}")
        return None, sitemap_url
