import argparse
from spider.utils import get_default_db_location


def create_parser():
    """
    Creates the argument parser and defines the available subcommands.
    """
    parser = argparse.ArgumentParser(
        prog="seo",
        description=(
            "SEOwayfinder is a user-friendly command-line tool that helps you crawl "
            "web pages, extract SEO metadata, and generate reports with ease."
        )
    )

    subparsers = parser.add_subparsers(dest='command', help='Available SEOwayfinder commands')

    # Crawl command
    parser_crawl = subparsers.add_parser(
        'crawl',
        help=(
            'Crawl a URL or sitemap to extract web page data such as titles, '
            'images, links, and more. If no URL is provided, it will use URLs from the clipboard.'
        )
    )
    parser_crawl.add_argument(
        'input',
        type=str,
        nargs='?',
        help="The URL or sitemap to crawl. If omitted, URLs from the clipboard will be used."
    )
    parser_crawl.add_argument(
        '-o', '--output',
        type=str,
        default=get_default_db_location(),
        help=(
            "Specify the output file path where the crawl results will be saved. "
            "Defaults to a file called 'output.txt' on your desktop."
        )
    )
    parser_crawl.add_argument(
        '-s', '--save',
        type=str,
        help="Save the crawl results to the database under a project name (www.example.com)."
    )

    # List command
    parser_list = subparsers.add_parser(
        'list',
        help=(
            'List all crawled projects stored in the SEOwayfinder database. '
            'Use this to view past crawls and retrieve project information.'
        )
    )

    # Get project data command
    parser_get = subparsers.add_parser(
        'get',
        help='Fetch all the pages data for a specific project from the database.'
    )
    parser_get.add_argument(
        'project_name',
        type=str,
        help="The name of the project to fetch data for."
    )

    # Remove project command
    parser_rm = subparsers.add_parser(
        'rm',
        help='Remove a specific project or all data from the SEOwayfinder database.'
    )
    parser_rm.add_argument(
        'project_name',
        type=str,
        nargs='?',
        help="The name of the project to remove. If omitted with --all, removes all projects."
    )
    parser_rm.add_argument(
        '--all',
        action='store_true',
        help="If provided, all projects and data will be removed from the database."
    )

    # Start Flask web dashboard command
    parser_dash = subparsers.add_parser('dash', help='Start the Flask dashboard for viewing project reports.')


    return parser
