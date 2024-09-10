import xml.etree.ElementTree as ET
import json
import asyncio
import os
from urllib.parse import urljoin, urlparse
from xml.etree.ElementTree import ParseError
from .schemas import PageData, Image
from .utils import validate_link_statuses, read_xml_file
from .crawler import fetch_sitemap_content, fetch_url_content, is_xml_content


def collect_and_process_sitemaps(sitemap_input, checked_links):
    """
    Collects and processes URLs from a given sitemap or local file, then crawls the URLs to extract SEO data.

    If the input is a valid URL, it fetches the sitemap or page content, determines whether it is an XML sitemap
    or an HTML page, and processes the links or data accordingly. It will skip already processed URLs and handle nested sitemaps.

    Args:
        sitemap_input (str): The URL or path to the sitemap file to process.
        checked_links (dict): A dictionary used to track and avoid rechecking the status of links.

    Returns:
        dict: A dictionary where the keys are page URLs and the values are the parsed data.
    """
    processed_sitemaps = set()
    all_pages_data = {}

    def process_sitemap(sitemap_url):
        """
        Processes an individual sitemap URL or page URL by fetching its content and parsing it.

        Args:
            sitemap_url (str): The URL to process.
        """
        print(f"Processing sitemap or page: {sitemap_url}")
        if sitemap_url in processed_sitemaps:
            print(f"Skipping already processed sitemap or page: {sitemap_url}")
            return
        processed_sitemaps.add(sitemap_url)

        content = asyncio.run(fetch_url_content(sitemap_url))
        if not content:
            print(f"No content found for: {sitemap_url}")
            return

        if is_xml_content(content, sitemap_url):
            print(f"Detected XML content for URL: {sitemap_url}")
            sitemap_urls, page_urls = extract_urls_from_xml_sitemap(content)

            print(f"Found {len(page_urls)} page URLs and {len(sitemap_urls)} nested sitemaps in {sitemap_url}")

            for page_url in page_urls:
                print(f"Processing page URL: {page_url}")
                page_data = extract_and_parse_page_data(page_url, checked_links)
                if page_data:
                    all_pages_data[page_url] = page_data

            for nested_sitemap_url in sitemap_urls:
                print(f"Processing nested sitemap: {nested_sitemap_url}")
                process_sitemap(nested_sitemap_url)

        else:
            print(f"Detected HTML content for URL: {sitemap_url}")
            page_data = extract_and_parse_page_data(sitemap_url, checked_links)
            if page_data:
                all_pages_data[sitemap_url] = page_data

    if urlparse(sitemap_input).scheme in ['http', 'https']:
        process_sitemap(sitemap_input)
    elif os.path.isfile(sitemap_input):
        xml_content = read_xml_file(sitemap_input)
        if xml_content:
            sitemap_urls, page_urls = extract_urls_from_xml_sitemap(xml_content)
            for page_url in page_urls:
                page_data = extract_and_parse_page_data(page_url, checked_links)
                if page_data:
                    all_pages_data[page_url] = page_data
            for loc in sitemap_urls:
                process_sitemap(loc)
    else:
        print("Invalid URL or file path")

    return all_pages_data


def extract_urls_from_xml_sitemap(xml_content):
    """
    Extracts page and sitemap URLs from an XML sitemap.

    Parses the given XML sitemap content and extracts URLs from both <sitemap> and <url> tags.

    Args:
        xml_content (str): The XML content of the sitemap.

    Returns:
        tuple: Two lists, one for sitemap URLs and one for page URLs.
    """
    try:
        root = ET.fromstring(xml_content)
    except ParseError as e:
        print(f"Failed to parse XML: {e}")
        return [], []

    namespace = {'ns': root.tag.split('}')[0].strip('{')}

    sitemap_urls = []
    page_urls = []

    sitemap_elements = root.findall('.//ns:sitemap/ns:loc', namespace)
    for elem in sitemap_elements:
        if elem.text:
            sitemap_urls.append(elem.text.strip())

    url_elements = root.findall('.//ns:url/ns:loc', namespace)
    for elem in url_elements:
        if elem.text:
            page_urls.append(elem.text.strip())

    return sitemap_urls, page_urls


def extract_and_parse_page_data(page_url, checked_links):
    """
    Crawls and parses an HTML page to extract SEO-relevant data such as meta descriptions, headings, links, and images.

    Args:
        page_url (str): The URL of the page to crawl and extract data from.
        checked_links (dict): A dictionary used to track and avoid rechecking the status of links.

    Returns:
        PageData: An object containing the extracted page data.
    """
    raw_page_data, base_url = fetch_sitemap_content(page_url)
    if not raw_page_data:
        return None

    title = raw_page_data.title.string.strip() if raw_page_data.title else ""

    meta_description_tag = raw_page_data.find('meta', attrs={'name': 'description'})
    meta_description = meta_description_tag.get('content', "").strip() if meta_description_tag else ""

    noindex = False
    robots_tag = raw_page_data.find('meta', attrs={'name': 'robots'})
    if robots_tag and 'noindex' in robots_tag.get('content', '').lower():
        noindex = True

    headings = {
        'h1': [h1.get_text(strip=True) for h1 in raw_page_data.find_all('h1')],
        'h2': [h2.get_text(strip=True) for h2 in raw_page_data.find_all('h2')],
        'h3': [h3.get_text(strip=True) for h3 in raw_page_data.find_all('h3')],
        'h4': [h4.get_text(strip=True) for h4 in raw_page_data.find_all('h4')],
        'h5': [h5.get_text(strip=True) for h5 in raw_page_data.find_all('h5')],
        'h6': [h6.get_text(strip=True) for h6 in raw_page_data.find_all('h6')],
    }

    hreflangs = [link.get('href') for link in raw_page_data.find_all('link', rel='alternate', hreflang=True)]

    structured_data = [
        json.loads(script.string.strip()) for script in raw_page_data.find_all('script', type='application/ld+json') if
        script.string
    ]

    robots = robots_tag.get('content', "").strip() if robots_tag else ""

    canonical_tag = raw_page_data.find('link', rel='canonical')
    canonical = canonical_tag.get('href', "").strip() if canonical_tag else ""

    links = [urljoin(base_url, a.get('href', '')) for a in raw_page_data.find_all('a', href=True)]

    non_200_links = validate_link_statuses(links, checked_links)

    parsed_base_url = urlparse(base_url)
    internal_links = []
    external_links = []
    for href in links:
        parsed_href = urlparse(href)
        if parsed_href.netloc == parsed_base_url.netloc:
            internal_links.append(href)
        else:
            external_links.append(href)

    images = [
        Image(src=urljoin(base_url, img.get('src', '')), alt=img.get('alt', "").strip()) for img in
        raw_page_data.find_all('img') if img.get('src')
    ]

    missing_alt_images = [img.src for img in images if not img.alt]

    paragraphs = [p.get_text(strip=True) for p in raw_page_data.find_all('p')]

    scripts = [urljoin(base_url, script.get('src', '')) for script in raw_page_data.find_all('script', src=True)]
    stylesheets = [urljoin(base_url, link.get('href', '')) for link in raw_page_data.find_all('link', rel='stylesheet', href=True)]

    parsed_url = urlparse(base_url)
    slug = '/' + parsed_url.path.lstrip('/')

    url_parts = {
        'params': parsed_url.params,
        'query': parsed_url.query,
        'fragment': parsed_url.fragment,
    }

    return PageData(
        title=title,
        meta_description=meta_description,
        headings=headings,
        links=links,
        images=images,
        paragraphs=paragraphs,
        scripts=scripts,
        stylesheets=stylesheets,
        slug=slug,
        url_parts=url_parts,
        canonical=canonical,
        robots=robots,
        structured_data=structured_data,
        hreflangs=hreflangs,
        internal_links=internal_links,
        external_links=external_links,
        noindex=noindex,
        non_200_links=non_200_links,
        missing_alt_images=missing_alt_images
    )
