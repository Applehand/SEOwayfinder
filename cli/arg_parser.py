import argparse
from spider.utils import get_default_output_file


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
        default=get_default_output_file(),
        help=(
            "Specify the output file path where the crawl results will be saved. "
            "Defaults to a file called 'output.txt' on your desktop."
        )
    )

    parser_list = subparsers.add_parser(
        'list',
        help=(
            'List all crawled projects stored in the SEOwayfinder database. '
            'Use this to view past crawls and retrieve project information.'
        )
    )

    return parser
