# SEOpus

**SEOpus** is a user-friendly command-line tool that simplifies SEO tasks by effortlessly parsing web page data. It streamlines the extraction of essential SEO insights for bulk analysis and optimization, making interaction with web data easier and more efficient.


## Features

- Parse sitemap URLs, XML files, or URLs from the clipboard.
- Crawl web pages and extract SEO-relevant data, including:
  - Meta descriptions
  - Page titles
  - Headings (H1-H6)
  - Links, Images, Scripts, and Stylesheets
  - URL slugs, query parameters, and fragments
  - Robots, HREflang, and canonical tags
  - Detect noindex directives
- Output results in a structured format for easy analysis.
- Seamlessly handles multiple URLs with caching of checked links to avoid redundant status checks.
- Supports JSON file output.

## Installation

To install the SEOpus tool from the GitHub repository:

1. Make sure you have Python installed on your system.
2. Install the package using `pip` by running:

```bash
pip install git+https://github.com/Applehand/SEOpus.git
```

Alternatively, you can clone the repository and install it locally:

```bash
git clone https://github.com/Applehand/SEOpus.git
cd SEOpus
pip install .
```

## Usage

Once installed, you can use the `seo` command in your terminal.

### Parsing a Sitemap URL:

To parse a sitemap URL and extract data:

```bash
seo crawl https://example.com/sitemap.xml
```

### Parsing a Local Sitemap XML File:

To parse a local sitemap XML file:

```bash
seo crawl /path/to/sitemap.xml
```

### Parsing URLs from the Clipboard:

You can also paste a sitemap or list of URLs directly from your clipboard using the `paste` command:

```bash
seo paste
```

### Saving Output:

You can specify the output file using the `-o` or `--output` option:

```bash
seo crawl https://example.com/sitemap.xml -o /path/to/output.json
```

By default, the output will be saved as `output.txt` on your desktop.

### Listing Projects (Future Functionality):

To list all projects in the database (coming soon):

```bash
seo list
```

## Contribution

Feel free to contribute to SEOpus by submitting issues or pull requests to the GitHub repository.

