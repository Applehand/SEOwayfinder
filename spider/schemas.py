from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import json


class Image(BaseModel):
    src: str
    alt: str


class PageData(BaseModel):
    title: str = ""
    meta_description: str = ""
    canonical: Optional[str] = None  # Canonical URL, if present
    robots: Optional[str] = None  # Robots meta tag, if present
    noindex: bool = False  # True if a noindex tag is found
    non_200_links: List[str] = Field(default_factory=list)  # List of links with non-200 status codes
    missing_alt_images: List[str] = Field(default_factory=list)  # List of images missing alt text
    structured_data: Optional[List[Dict]] = Field(default_factory=list)  # Structured data (JSON-LD or Microdata)
    headings: Dict[str, List[str]] = Field(default_factory=dict)  # Dictionary for headings h1-h6
    links: List[str] = Field(default_factory=list)  # All links
    internal_links: List[str] = Field(default_factory=list)  # Internal links only
    external_links: List[str] = Field(default_factory=list)  # External links only
    hreflang: Dict[str, str] = Field(default_factory=dict)  # Dictionary for hreflang attributes
    images: List[Image] = Field(default_factory=list)  # List of images
    paragraphs: List[str] = Field(default_factory=list)  # Extracted paragraphs
    scripts: List[str] = Field(default_factory=list)  # JavaScript file links
    stylesheets: List[str] = Field(default_factory=list)  # CSS file links
    slug: str = ""  # Slug from URL
    url_parts: Dict[str, Optional[str]] = Field(default_factory=dict)  # Combination of params, query, and fragments on a URL
