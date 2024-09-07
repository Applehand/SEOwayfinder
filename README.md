# SEOpus

**SEOpus** is a user-friendly command-line tool that simplifies SEO tasks by effortlessly parsing web page data. It streamlines the extraction of essential SEO insights for bulk analysis and optimization, making interaction with web data easier and more efficient.

## Features

- Parse XML sitemaps and URLs.
- Crawl web pages and extract SEO-relevant data, including:
  - Meta descriptions
  - Page titles
  - Headings (H1-H6)
  - Links, Images, Scripts, and Stylesheets
  - URL slugs, query parameters, and fragments
  - Robots, HREflang, and canonical tags
  - Detect noindex directives
- Output results in a structured format for easy analysis.
- Supports JSON file output.

## Installation

To install the SEOpus tool from the GitHub repository:

1. Make sure you have [Python](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads) installed on your system.
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

### Parsing URLs from the Clipboard:

You can also paste a sitemap or list of URLs directly from your clipboard using the `paste` command:

```bash
seo paste
```

### Parsing a Local Sitemap XML File:

To parse a local sitemap XML file:

```bash
seo crawl /path/to/sitemap.xml
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

## Roadmap

- **SQLite Database Integration**: Store parsed results for projects locally for easy retrieval.
- **HTML Report Generation**: Automatically generate and open a detailed SEO report in your browser.
- **Tech Work Spreadsheet**: Automatically generate a template for technical SEO tasks based on crawl results.
- **Interactive Web Dashboard**: Provide an interactive web-based UI for querying and visualizing the data stored in the database.
- **Advanced Filtering and Search**: Allow users to filter and search parsed data within the command line or web dashboard.

## Contribution

Feel free to contribute to SEOpus by submitting issues or pull requests to the GitHub repository.
