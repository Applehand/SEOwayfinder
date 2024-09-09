# SEOpus

![The Digital Compass](https://github.com/Applehand/SEOpus/blob/master/assets/digital_compass.jpeg)

> "The real voyage of discovery consists not in seeking new landscapes, but in having new eyes."  
> — Marcel Proust

**SEOpus** offers a simple command-line solution to streamline SEO tasks by efficiently parsing web page data. It optimizes the extraction of critical SEO insights for bulk analysis, ensuring smoother and faster interaction with web data.


## Features

- Crawl web pages directly or via a sitemap to extract key SEO data, including:
  - Page titles
  - Meta descriptions
  - Headings (H1-H6)
  - Links, images, scripts, and stylesheets
  - URL slugs, query parameters, and fragments
  - Robots, HREflang, canonical tags, and noindex directives
- Output results in a structured, easy-to-read dashboard format for efficient analysis.
- Generate an Excel sheet with actionable technical SEO recommendations ("tech work") to fix issues identified during the crawl.


### Installation Instructions

To install the **SEOpus** tool, follow these steps:

1. **Ensure You Have Python and Git Installed:**

   - **Python**: You’ll need Python, a popular programming language, installed on your system. You can download and install it from the [official Python website](https://www.python.org/downloads/). Python is available for Windows, macOS, and Linux.

   - **Add Python to PATH**: During the Python installation process, you’ll see an option to "Add Python to PATH" in the installation window. Make sure this box is checked before you proceed with the installation. This step is very important because it allows you to run Python from the terminal or command prompt.

     - If you forget to check this option, don’t worry! You can manually add Python to your system's PATH by following [this guide](https://realpython.com/add-python-to-path/). Without this, you won’t be able to run the `python` or `pip` commands from the terminal.

   - **Verify Installation**: To check if Python is installed on your machine, open a terminal (on Windows, you can use PowerShell or Command Prompt; on macOS or Linux, use the Terminal app) and run the following command:

       ```bash
       python --version
       ```

       If Python is installed, you’ll see the version number. If not, follow the installation guide on the Python website.

   - **Git**: Git is a version control tool that helps manage code. You can download Git from the [Git website](https://git-scm.com/downloads). Follow the installation instructions for your operating system.

     - **Verify Installation**: After installing Git, check if it’s working by running this command in your terminal:

       ```bash
       git --version
       ```

       You should see the Git version number.

2. **Install SEOpus Using Python’s Package Manager (pip):**

   Once you have Python and Git installed, you’ll use Python’s package manager, `pip`, to install **SEOpus**. `pip` comes bundled with Python, so you don’t need to install it separately. 

   Here’s what you need to do:

   1. **Open a Terminal**: On Windows, use PowerShell or Command Prompt. On macOS or Linux, use the Terminal app.

   2. **Run the Following Command**: This command will install SEOpus directly from the GitHub repository:

      ```bash
      pip install git+https://github.com/Applehand/SEOpus.git
      ```

   3. **Verify Installation**: After the installation is complete, check if SEOpus is installed by running:

      ```bash
      seo --help
      ```

      If the tool is installed correctly, you’ll see a list of available commands and options for SEOpus.

---

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
- **Publish to PyPI**: Publishing to the Python Package Index to allow installation with `pip install seopus`. 

## Contribution

Feel free to contribute to SEOpus by submitting issues or pull requests to the GitHub repository.
