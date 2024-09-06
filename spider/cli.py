import os
import argparse
from urllib.parse import urlparse

from .extractor import extract_urls_from_sitemap, extract_page_data
from .crawler import crawl_sitemap_url
from . import utils


def handle_sitemap_input(sitemap_input):
    sitemap_url_list = []
    if urlparse(sitemap_input).scheme in ['http', 'https']:
        # Handle as URL
        xml_content = utils.get_response_text(sitemap_input)
        if xml_content:
            locs = extract_urls_from_sitemap(xml_content)
            for loc in locs:
                sitemap_url_list.append(loc)
    elif os.path.isfile(sitemap_input):
        # Handle as file path
        xml_content = utils.read_sitemap_file(sitemap_input)
        if xml_content:
            locs = extract_urls_from_sitemap(xml_content)
            for loc in locs:
                sitemap_url_list.append(loc)
    else:
        print("Invalid URL or file path")

    return sitemap_url_list


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
    sitemap_urls = handle_sitemap_input(args.sitemap_input)

    all_refined_page_data = []
    for url in sitemap_urls:
        raw_page_data, base_url = crawl_sitemap_url(url)
        if raw_page_data:
            refined_data = extract_page_data(raw_page_data, base_url)
            all_refined_page_data.append(refined_data)
