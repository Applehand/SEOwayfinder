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
            "sitemaps, extract SEO metadata, and generate reports with ease. "
            "Use this tool to analyze web page data in bulk and optimize your site's SEO."
        )
    )

    subparsers = parser.add_subparsers(dest='command', help='Available SEOwayfinder commands')

    parser_crawl = subparsers.add_parser(
        'crawl',
        help=(
            'Crawl a sitemap URL or local XML file, extract metadata such as meta descriptions, '
            'page titles, headings, and more. Use the -o option to save the output to a file.'
        )
    )
    parser_crawl.add_argument(
        'input',
        type=str,
        help="The URL of the sitemap to crawl or the path to a local sitemap XML file"
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

    parser_paste = subparsers.add_parser(
        'paste',
        help=(
            'Crawl a list of URLs or a sitemap copied to your clipboard. '
            'SEOwayfinder will automatically crawl and extract SEO data from these URLs.'
        )
    )
    parser_paste.add_argument(
        '-o', '--output',
        type=str,
        default=get_default_output_file(),
        help=(
            "Specify the output file path where the results will be saved. "
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
