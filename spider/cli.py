import os
import argparse
from urllib.parse import urlparse
import time

from .extractor import extract_urls_from_xml, extract_page_data
from .crawler import crawl_sitemap_url
from . import utils


def handle_sitemap_input(sitemap_input):
    sitemap_urls = []
    processed_sitemaps = []

    def process_sitemap(sitemap_url):
        if sitemap_url in processed_sitemaps:
            print(f"Skipping already processed sitemap: {sitemap_url}")
            return
        processed_sitemaps.append(sitemap_url)
        xml_content = utils.get_response_text(sitemap_url)
        if xml_content:
            locs = extract_urls_from_xml(xml_content)
            for loc in locs:
                if loc.endswith('.xml'):
                    print(f"Processing Sitemap: {loc}")
                    process_sitemap(loc)
                else:
                    sitemap_urls.append(loc)

    if urlparse(sitemap_input).scheme in ['http', 'https']:
        process_sitemap(sitemap_input)
    elif os.path.isfile(sitemap_input):
        xml_content = utils.read_sitemap_file(sitemap_input)
        if xml_content:
            locs = extract_urls_from_xml(xml_content)
            for loc in locs:
                if loc.endswith('.xml'):
                    process_sitemap(loc)
                else:
                    sitemap_urls.append(loc)
    else:
        print("Invalid URL or file path")

    return sitemap_urls


def process_urls(sitemap_urls):
    all_page_data = {}
    for url in sitemap_urls:
        time.sleep(1)
        raw_page_data, base_url = crawl_sitemap_url(url)
        if raw_page_data:
            refined_data = extract_page_data(raw_page_data, base_url)
            all_page_data[base_url] = refined_data.dict()
    return all_page_data


def main():
    parser = argparse.ArgumentParser(
        prog="seo",
        description="An SEO command-line interface tool for parsing sitemaps and URLs"
    )

    parser.add_argument(
        'input',
        type=str,
        help="The URL of the sitemap or the 'paste' command to process clipboard data."
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=utils.get_default_output_file(),
        help='The output file path. Defaults to output.txt on your desktop.'
    )

    args = parser.parse_args()
    output_file_location = args.output

    if args.input == 'paste':
        sitemap_urls = utils.handle_paste_from_clipboard()
        refined_page_data = process_urls(sitemap_urls)
        utils.write_to_file(refined_page_data, output_file_location)
    else:
        sitemap_urls = handle_sitemap_input(args.input)
        refined_page_data = process_urls(sitemap_urls)
        utils.write_to_file(refined_page_data, output_file_location)

