import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse
from xml.etree.ElementTree import ParseError
from .schemas import PageData, Image


def extract_urls_from_sitemap(xml_content):
    try:
        root = ET.fromstring(xml_content)
    except ParseError as e:
        print(f"Failed to parse XML: {e}")
        return []

    # Extract the namespace, if present
    namespace = {}
    for elem in root.iter():
        if '}' in elem.tag:
            namespace_uri = elem.tag.split('}', 1)[0].strip('{')
            namespace['ns'] = namespace_uri
            break

    # Find all 'loc' elements, handling namespaces
    loc_elements = root.findall('.//ns:loc', namespace)
    return [loc.text for loc in loc_elements]


def extract_page_data(page, base_url: str) -> PageData:
    if not page:
        return PageData()  # Return an empty PageData if page is None

    # Extract title
    title = page.title.string.strip() if page.title else ""

    # Extract meta description
    meta_description_tag = page.find('meta', attrs={'name': 'description'})
    meta_description = meta_description_tag.get('content', "").strip() if meta_description_tag else ""

    # Extract headings
    headings = {
        'h1': [h1.get_text(strip=True) for h1 in page.find_all('h1')],
        'h2': [h2.get_text(strip=True) for h2 in page.find_all('h2')],
        'h3': [h3.get_text(strip=True) for h3 in page.find_all('h3')],
        'h4': [h4.get_text(strip=True) for h4 in page.find_all('h4')],
        'h5': [h5.get_text(strip=True) for h5 in page.find_all('h5')],
        'h6': [h6.get_text(strip=True) for h6 in page.find_all('h6')],
    }

    # Extract links (convert relative URLs to absolute)
    links = [urljoin(base_url, a.get('href')) for a in page.find_all('a', href=True)]

    # Extract images
    images = [Image(src=urljoin(base_url, img.get('src')), alt=img.get('alt', "").strip()) for img in page.find_all('img') if img.get('src')]

    # Extract paragraphs
    paragraphs = [p.get_text(strip=True) for p in page.find_all('p')]

    # Extract scripts and stylesheets
    scripts = [urljoin(base_url, script.get('src')) for script in page.find_all('script', src=True)]
    stylesheets = [urljoin(base_url, link.get('href')) for link in page.find_all('link', rel='stylesheet', href=True)]

    # Example slug extraction from URL
    parsed_url = urlparse(base_url)
    slug = '/' + parsed_url.path.lstrip('/')

    # Extract params, query, and fragment
    params = parsed_url.params
    query = parsed_url.query
    fragment = parsed_url.fragment

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
        params=params,
        query=query,
        fragment=fragment
    )
