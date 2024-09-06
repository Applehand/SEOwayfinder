from typing import List, Dict, Optional, Union
from pydantic import BaseModel


class Image(BaseModel):
    src: str
    alt: str


class PageData(BaseModel):
    title: str = ""
    meta_description: str = ""
    canonical: Optional[str] = None  # Canonical URL, if present
    robots: Optional[str] = None  # Robots meta tag, if present
    structured_data: Optional[List[Dict]] = {}  # Structured data (JSON-LD or Microdata), default as empty dictionary
    headings: Dict[str, List[str]] = {}  # Dictionary for headings h1-h6
    links: List[str] = []  # All links
    internal_links: List[str] = []  # Internal links only
    external_links: List[str] = []  # External links only
    hreflang: Dict[str, str] = {}  # Dictionary for hreflang attributes (language-region: URL)
    images: List[Image] = []  # List of images
    paragraphs: List[str] = []  # Extracted paragraphs
    scripts: List[str] = []  # JavaScript file links
    stylesheets: List[str] = []  # CSS file links
    slug: str = ""  # Slug from URL
    url_parts: Dict[str, Optional[str]] = {}  # Combination of params, query, and fragments on a URL


