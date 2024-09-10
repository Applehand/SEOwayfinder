from spider.utils import fetch_urls_from_clipboard, save_json_to_file
from spider.extractor import collect_and_process_sitemaps, extract_and_parse_page_data
from spider.storage import save_page_data, fetch_all_project_names, fetch_pages_by_project, clear_all_data
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
    project_name = args.save if args.save else None

    for page_url in page_urls:
        if page_url.endswith('.xml'):
            all_page_data.update(collect_and_process_sitemaps(page_url, checked_links))
        else:
            page_data = extract_and_parse_page_data(page_url, checked_links)
            if page_data:
                all_page_data[page_url] = page_data

                if project_name:
                    save_page_data(project_name, page_data)
                else:
                    print(f"No project name: {project_name}")

    print(fetch_pages_by_project(project_name))
    # save_json_to_file(all_page_data, args.output)


def handle_list_command():
    """
    Handle the 'list' command.

    This function lists all crawled projects stored in the database.
    """
    project_names = fetch_all_project_names()

    if not project_names:
        print("No projects found in the database.")
    else:
        print("Crawled Projects:")
        for project in project_names:
            print(f"- {project}")


def handle_clear_command():
    """
    Handle the 'cleardb' command.

    This function clears all data from the 'projects' and 'pages' tables in the database.

    Args:
        None

    Returns:
        None
    """
    clear_all_data()


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
    elif args.command == 'rm':
        handle_clear_command()
