import argparse
from spider.utils import get_default_output_file


def create_parser():
    """
    Creates the argument parser and defines the available subcommands.
    """
    parser = argparse.ArgumentParser(
        prog="seo",
        description="SEO Crawler CLI Tool. Use this tool to crawl sitemaps, extract metadata, and generate reports."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Crawl command
    parser_crawl = subparsers.add_parser('crawl', help='Crawl a sitemap and extract data')
    parser_crawl.add_argument('input', type=str, help="The URL of the sitemap to crawl")
    parser_crawl.add_argument('-o', '--output', type=str, default=get_default_output_file(), help="The output file path")

    # Paste command
    parser_paste = subparsers.add_parser('paste', help='Crawl URLs or sitemap data from clipboard')
    parser_paste.add_argument('-o', '--output', type=str, default=get_default_output_file(), help="The output file path")

    # List projects command
    parser_list = subparsers.add_parser('list', help='List all projects in the database')

    return parser
