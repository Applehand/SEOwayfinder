from spider.utils import fetch_urls_from_clipboard, save_json_to_file
from spider.extractor import collect_and_process_sitemaps, extract_and_parse_page_data
from .arg_parser import create_parser


def handle_crawl_command(args):
    """
    Handle the 'crawl' command.

    This function is responsible for crawling a sitemap or URLs provided via input or clipboard.
    If no input is provided, it automatically grabs URLs from the clipboard.

    Args:
        args (Namespace): Parsed command-line arguments.

    Returns:
        None
    """
    checked_links = dict()

    if args.input:
        page_urls = [args.input]
    else:
        page_urls = fetch_urls_from_clipboard()

    if not page_urls:
        print("No valid URLs provided or found in clipboard.")
        return

    all_page_data = {}

    for page_url in page_urls:
        if page_url.endswith('.xml'):
            all_page_data.update(collect_and_process_sitemaps(page_url, checked_links))
        else:
            page_data = extract_and_parse_page_data(page_url, checked_links)
            if page_data:
                all_page_data[page_url] = page_data

    save_json_to_file(all_page_data, args.output)


def handle_list_command():
    """
    Handle the 'list' command.

    This function is responsible for listing all crawled projects stored in the database.
    (This functionality is a placeholder and needs to be implemented.)

    Args:
        None

    Returns:
        None
    """
    print("Listing all projects in the database...")


def execute_command():
    """
    Execute the appropriate command based on user input.

    This function parses the command-line arguments and executes the corresponding
    command (crawl, paste, list). If no valid command is provided, it displays help.

    Args:
        None

    Returns:
        None
    """
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return
    if args.command == 'crawl':
        handle_crawl_command(args)
    elif args.command == 'list':
        handle_list_command()
