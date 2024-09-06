import argparse
import os
import xml.etree.ElementTree as ET
import requests
from urllib.parse import urlparse
from xml.etree.ElementTree import ParseError


def get_sitemap(url):
    try:
        response = requests.get(url)
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


def parse_sitemap(xml_content):
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


def process_sitemap(sitemap_input):
    if urlparse(sitemap_input).scheme in ['http', 'https']:
        # Handle as URL
        xml_content = get_sitemap(sitemap_input)
        if xml_content:
            locs = parse_sitemap(xml_content)
            print("URLs from sitemap:")
            for loc in locs:
                print(loc)
    elif os.path.isfile(sitemap_input):
        # Handle as file path
        xml_content = read_sitemap_file(sitemap_input)
        if xml_content:
            locs = parse_sitemap(xml_content)
            print("URLs from sitemap:")
            for loc in locs:
                print(loc)
    else:
        print("Invalid URL or file path")


def main():
    parser = argparse.ArgumentParser(
        prog="seo",
        description="An SEO command-line interface tool for parsing sitemap URLs or file paths"
    )

    parser.add_argument(
        'sitemap_input',
        type=str,
        help='The URL or file path of the sitemap to process'
    )

    args = parser.parse_args()
    process_sitemap(args.sitemap_input)


if __name__ == "__main__":
    main()
