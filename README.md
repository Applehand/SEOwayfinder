# SEOcli

**SEOcli** is a command-line tool for parsing web page data from URLs in a sitemap or from clipboard input. This tool is ideal for quickly analyzing web pages in bulk and extracting essential SEO data for optimization purposes.

## Features

- Parse sitemap URLs, XML files, or URLs from the clipboard.
- Crawl web pages and extract SEO-relevant data, including:
  - Meta descriptions
  - Page titles
  - Headings (H1-H6)
  - Links, Images, Scripts, and Stylesheets
  - URL slugs, query parameters, and fragments
  - Robots, HREflang, canonicals
- Output results in a structured format for further analysis.

## Installation

To install the SEOcli tool from the GitHub repository:

1. Make sure you have Python installed on your system.
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

### Parsing a Sitemap URL:

To parse a sitemap URL and extract data:

```bash
seo https://example.com/sitemap.xml
```

### Parsing a Local Sitemap XML File:

To parse a local sitemap XML file (ensure the file is available on the path):

```bash
seo /path/to/sitemap.xml
```

### Parsing URLs from the Clipboard:

You can also paste a list of URLs directly from your clipboard using the `paste` command. This is useful if you already have a list of URLs to process:

```bash
seo paste
```

Ensure that your clipboard contains valid URLs, one per line, before running this command (copy from a spreadsheet).

### Saving Output:

You can specify the output file using the `-o` or `--output` option:

```bash
seo https://example.com/sitemap.xml -o /path/to/output.json
```

By default, the output will be saved as `output.txt` on your desktop.
