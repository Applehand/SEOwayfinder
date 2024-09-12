# SEOwayfinder

> "The only true voyage of discovery, the only fountain of Eternal Youth, would be not to visit strange lands but to possess other eyes, to behold the universe through the eyes of another, of a hundred others, to behold the hundred universes that each of them beholds, that each of them is;"  
> — Marcel Proust

**SEOwayfinder** simplifies SEO tasks with a command-line tool and web dashboard that allows users to efficiently crawl, parse, view, and analyze web page data for bulk SEO insights.

## Features

- Crawl URLs or sitemaps to extract SEO metadata such as:
  - Page titles, meta descriptions, and headings (H1-H6)
  - Links (internal and external), images, and structured data
  - URL slugs, query parameters, and fragments
  - Canonical tags, robots directives, noindex tags, and HREFlang attributes
- View detailed SEO insights through a web dashboard, enabling project-based browsing of crawl results.
- Export results to JSON for external analysis.
- Track SEO data for multiple projects using a built-in SQLite database.
- JavaScript rendering support for fully crawling pages with dynamic content.

### Installation Instructions

To install the **SEOwayfinder** tool, follow these steps:

1. **Ensure You Have [Python](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads) installed and on your PATH**

2. **Install SEOwayfinder Using `pip`:**

   1. **Run the Following Command**: This command will install SEOwayfinder directly from the GitHub repository:

      ```bash
      pip install git+https://github.com/Applehand/SEOwayfinder.git
      ```

   2. **Verify Installation**: After the installation is complete, check if SEOwayfinder is installed by running:

      ```bash
      seo
      ```

      If the tool is installed correctly, you’ll see a list of available commands and options for SEOwayfinder.

---

## Usage

## Starting the Flask Web App Locally

To run the web interface for SEOwayfinder, run:

```bash
seo dash
```

This will open the dashboard in your browser at http://127.0.0.1:5000/.


### Parsing a Sitemap URL:

To parse a sitemap URL and extract data:

```bash
seo crawl https://example.com/sitemap.xml
```

### Parsing URLs from the Clipboard:

You can also paste a sitemap or list of URLs directly from your clipboard:

```bash
seo crawl
```

### Parsing a Local Sitemap XML File:

To parse a local sitemap XML file:

```bash
seo crawl /path/to/sitemap.xml
```

### Listing Projects:

To list all projects in the database:

```bash
seo list
```

### Removing a Project:

To remove a project from the database:

```bash
seo rm <project_name>
```

## Roadmap

- ~~**SQLite Database Integration**: Optionally store parsed results for projects locally for easy retrieval. (`seo crawl -s`)~~
- **Tech Work Recs**: Generate a web view for implementing SEO fixes based on crawl results, with a cli and web option to export to spreadsheet. (`seo crawl -w`)
- ~~**Simple Web Dashboard**: Provide a basic web UI for viewing projects and the data stored in the database.~~(`seo dash`)
- **Advanced Filtering and Search**: Allow users to filter and search parsed data within the command line or web dashboard.
- **Asynchronous Parsing**: Run crawling processes in async with Scrapy, a more performant crawling library.
- **Upgrade to HTTPX**: Replace Requests library with HTTPX, a more performant and modern async library.
- ~~**Render Page Javascript**: Render JavaScript for a more accurate html extraction and robust crawler.~~
- **Publish to PyPI**: Publishing to the Python Package Index to allow installation with `pip install seowayfinder`. 

## Contribution

Feel free to contribute to SEOwayfinder by submitting issues or pull requests to the GitHub repository.
