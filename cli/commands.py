from spider.utils import fetch_urls_from_clipboard, save_json_to_file
from spider.extractor import collect_and_process_sitemaps, extract_and_parse_page_data
from .arg_parser import create_parser


def handle_crawl_command(args):
    checked_links = dict()
    all_page_data = collect_and_process_sitemaps(args.input, checked_links)
    save_json_to_file(all_page_data, args.output)


def handle_paste_command(output_file_location):
    checked_links = dict()
    page_urls = fetch_urls_from_clipboard()

    if not page_urls:
        print("No valid URLs found in clipboard.")
        return

    all_page_data = {}

    for page_url in page_urls:
        if page_url.endswith('.xml'):
            all_page_data.update(collect_and_process_sitemaps(page_url, checked_links))
        else:
            page_data = extract_and_parse_page_data(page_url, checked_links)
            if page_data:
                all_page_data[page_url] = page_data

    save_json_to_file(all_page_data, output_file_location)


def handle_list_command():
    print("Listing all projects in the database...")


def execute_command():
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return
    if args.command == 'crawl':
        handle_crawl_command(args)
    elif args.command == 'paste':
        handle_paste_command(args.output)
    elif args.command == 'list':
        handle_list_command()
