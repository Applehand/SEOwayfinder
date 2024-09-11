import json
import os
import subprocess
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


def handle_get_command(project_name):
    """
    Handle the 'get' command to fetch project data from the database.

    Args:
        project_name (str): The name of the project to fetch data for.

    Returns:
        pages (list): A list of pages for the project or an empty list if not found.
    """
    if not project_name:
        return None, "Please provide a project name."

    pages = fetch_pages_by_project(project_name)

    if not pages:
        return None, f"No data found for project '{project_name}'."

    return pages


def handle_dash_command():
    """
    Handle the 'dash' command to start the Flask web dashboard.
    """
    # Set the environment variable FLASK_APP to your main Flask app
    os.environ['FLASK_APP'] = 'main.py'

    # Start the Flask server using subprocess
    try:
        subprocess.run(["flask", "run"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start the Flask server: {e}")
    except FileNotFoundError:
        print("Flask command not found. Make sure Flask is installed.")


def execute_command():
    """
    Execute the appropriate command based on user input (CLI context).

    This function parses the command-line arguments and executes the corresponding
    command (crawl, get, list). If no valid command is provided, it displays help.

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
        project_name = args.project_name
        pages = handle_get_command(project_name)
        print(f"Pages for project '{project_name}':")
        for page in pages:
            print(json.dumps(page, indent=4))
    elif args.command == 'list':
        handle_list_command()
    elif args.command == 'rm':
        handle_clear_command()
    elif args.command == 'dash':
        handle_dash_command()

