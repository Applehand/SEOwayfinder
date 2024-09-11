import json
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

    project_name = args.save if args.save else None

    if project_name:
        print(f"Saving results under project name: {project_name}")
    else:
        print("No project name provided. Results will not be saved to the database.")

    all_page_data = {}

    for page_url in page_urls:
        if page_url.endswith('.xml'):
            sitemap_data = collect_and_process_sitemaps(page_url, checked_links)
            if sitemap_data:
                all_page_data.update(sitemap_data)
                if project_name:
                    for url, page_data in sitemap_data.items():
                        save_page_data(project_name, page_data)
        else:
            page_data = extract_and_parse_page_data(page_url, checked_links)
            if page_data:
                all_page_data[page_url] = page_data
                if project_name:
                    save_page_data(project_name, page_data)

    # if args.output:
    #     save_json_to_file(all_page_data, args.output)


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


def handle_get_command(args):
    """
    Handle the 'get' command.

    This function fetches all the pages for a specific project from the database
    and prints them in a readable format.

    Args:
        args (Namespace): Parsed command-line arguments containing the project name.

    Returns:
        None
    """
    project_name = args.project_name

    if not project_name:
        print("Please provide a project name.")
        return

    pages = fetch_pages_by_project(project_name)

    if not pages:
        print(f"No data found for project '{project_name}'.")
    else:
        print(f"Pages for project '{project_name}':")
        for page in pages:
            print(json.dumps(page, indent=4))


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
    elif args.command == 'crawl':
        handle_crawl_command(args)
    elif args.command == "get":
        handle_get_command(args)
    elif args.command == 'list':
        handle_list_command()
    elif args.command == 'rm':
        handle_clear_command()

