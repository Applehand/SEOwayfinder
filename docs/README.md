# SEOcli

**SEOcli** is a command-line tool for parsing web page data from URLs in a sitemap. This tool is ideal for quickly analyzing web pages in bulk and extracting essential SEO data.

## Features

- Parse sitemap URLs or XML files.
- Crawl pages and extract SEO-relevant data:
  - Meta descriptions
  - Page titles
  - Headings (H1-H6)
  - Links, Images, Scripts, and Stylesheets
  - URL slugs, query parameters, and fragments
  - Robots, HREflang, canonicals
- Output results in a structured format.

## Installation

To install the SEOcli tool from the GitHub repository:

1. Make sure you have Python installed on your system
2. Install the package using `pip` by running:

```bash
pip install git+https://github.com/Applehand/SEOcli.git
```

Alternatively, you can clone the repository and install it locally:

```bash
git clone https://github.com/Applehand/SEOcli.git
cd SEOcli
pip install .
```

## Usage

Once installed, you can use the `seo` command in your terminal.

### Example:

To parse a sitemap URL and extract data:

```bash
seo https://example.com/sitemap.xml
```

To parse a local sitemap XML file (.xml file must be in project directory):

```bash
seo /path/to/sitemap.xml
```

The tool will crawl the sitemap and output relevant SEO information such as meta descriptions, page titles, headings, and other data for each URL.

