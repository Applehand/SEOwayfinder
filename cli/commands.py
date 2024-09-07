import argparse
from spider.utils import get_default_output_file, fetch_urls_from_clipboard, save_json_to_file
from spider.extractor import collect_and_process_sitemaps, extract_and_parse_page_data


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
        default=get_default_output_file(),
        help='The output file path. Defaults to output.txt on your desktop.'
    )

    args = parser.parse_args()
    output_file_location = args.output

    checked_links = dict()  # To avoid requesting the status of on-page links multiple times

    if args.input == 'paste':
        page_urls = fetch_urls_from_clipboard()
        all_page_data = {}
        for page_url in page_urls:
            page_data = extract_and_parse_page_data(page_url, checked_links)
            if page_data:
                all_page_data[page_url] = page_data
    else:
        all_page_data = collect_and_process_sitemaps(args.input, checked_links)

    save_json_to_file(all_page_data, output_file_location)
