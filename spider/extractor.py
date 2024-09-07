import xml.etree.ElementTree as ET
import json
import os
import time
from urllib.parse import urljoin, urlparse
from xml.etree.ElementTree import ParseError
from .schemas import PageData, Image
from .utils import validate_link_statuses, read_xml_file
from .crawler import fetch_sitemap_content, fetch_url_content


def collect_and_process_sitemaps(sitemap_input, checked_links):
    processed_sitemaps = set()
    all_pages_data = {}

    def process_sitemap(sitemap_url):
        print(f"Processing sitemap: {sitemap_url}")
        if sitemap_url in processed_sitemaps:
            print(f"Skipping already processed sitemap: {sitemap_url}")
            return
        processed_sitemaps.add(sitemap_url)

        # Fetch the sitemap content and parse it
        xml_content = fetch_url_content(sitemap_url)
        if not xml_content:
            print(f"No content found for sitemap: {sitemap_url}")
            return

        sitemap_urls, page_urls = extract_urls_from_xml_sitemap(xml_content)

        # Log how many URLs are being processed
        print(f"Found {len(page_urls)} page URLs and {len(sitemap_urls)} nested sitemaps in {sitemap_url}")

        # Process the page URLs found in the sitemap
        for page_url in page_urls:
            print(f"Processing page URL: {page_url}")
            page_data = extract_and_parse_page_data(page_url, checked_links)
            if page_data:
                all_pages_data[page_url] = page_data

        # Recursively process nested sitemaps
        for nested_sitemap_url in sitemap_urls:
            print(f"Processing nested sitemap: {nested_sitemap_url}")
            process_sitemap(nested_sitemap_url)

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
    try:
        root = ET.fromstring(xml_content)
    except ParseError as e:
        print(f"Failed to parse XML: {e}")
        return []

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
    # Delay to avoid overloading the server
    time.sleep(1)

    raw_page_data, base_url = fetch_sitemap_content(page_url)
    if not raw_page_data:
        return None

    # Extract title
    title = raw_page_data.title.string.strip() if raw_page_data.title else ""

    # Extract meta description
    meta_description_tag = raw_page_data.find('meta', attrs={'name': 'description'})
    meta_description = meta_description_tag.get('content', "").strip() if meta_description_tag else ""

    # Check for noindex
    noindex = False
    robots_tag = raw_page_data.find('meta', attrs={'name': 'robots'})
    if robots_tag and 'noindex' in robots_tag.get('content', '').lower():
        noindex = True

    # Extract headings
    headings = {
        'h1': [h1.get_text(strip=True) for h1 in raw_page_data.find_all('h1')],
        'h2': [h2.get_text(strip=True) for h2 in raw_page_data.find_all('h2')],
        'h3': [h3.get_text(strip=True) for h3 in raw_page_data.find_all('h3')],
        'h4': [h4.get_text(strip=True) for h4 in raw_page_data.find_all('h4')],
        'h5': [h5.get_text(strip=True) for h5 in raw_page_data.find_all('h5')],
        'h6': [h6.get_text(strip=True) for h6 in raw_page_data.find_all('h6')],
    }

    # Extract hreflang tags
    hreflangs = [link.get('href') for link in raw_page_data.find_all('link', rel='alternate', hreflang=True)]

    # Extract structured data (JSON-LD)
    structured_data = [
        json.loads(script.string.strip()) for script in raw_page_data.find_all('script', type='application/ld+json') if
        script.string
    ]

    # Extract robots meta tag
    robots = robots_tag.get('content', "").strip() if robots_tag else ""

    # Extract canonical URL
    canonical_tag = raw_page_data.find('link', rel='canonical')
    canonical = canonical_tag.get('href', "").strip() if canonical_tag else ""

    # Extract links (convert relative URLs to absolute)
    links = [urljoin(base_url, a.get('href', '')) for a in raw_page_data.find_all('a', href=True)]

    # Check link statuses
    non_200_links = validate_link_statuses(links, checked_links)

    # Classify links as internal or external
    parsed_base_url = urlparse(base_url)
    internal_links = []
    external_links = []
    for href in links:
        parsed_href = urlparse(href)
        if parsed_href.netloc == parsed_base_url.netloc:
            internal_links.append(href)
        else:
            external_links.append(href)

    # Extract images
    images = [
        Image(src=urljoin(base_url, img.get('src', '')), alt=img.get('alt', "").strip()) for img in
        raw_page_data.find_all('img') if img.get('src')
    ]

    # Check if images are missing alt text
    missing_alt_images = [img.src for img in images if not img.alt]

    # Extract paragraphs
    paragraphs = [p.get_text(strip=True) for p in raw_page_data.find_all('p')]

    # Extract scripts and stylesheets
    scripts = [urljoin(base_url, script.get('src', '')) for script in raw_page_data.find_all('script', src=True)]
    stylesheets = [urljoin(base_url, link.get('href', '')) for link in
                   raw_page_data.find_all('link', rel='stylesheet', href=True)]

    # Extract the slug from the URL
    parsed_url = urlparse(base_url)
    slug = '/' + parsed_url.path.lstrip('/')

    # Extract URL parameters, query, and fragment
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

