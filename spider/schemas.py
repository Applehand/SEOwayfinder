from typing import List
from pydantic import BaseModel


class Image(BaseModel):
    src: str
    alt: str


class PageData(BaseModel):
    title: str = ""
    meta_description: str = ""
    headings: dict = {}
    links: List[str] = []
    images: List[Image] = []
    paragraphs: List[str] = []
    scripts: List[str] = []
    stylesheets: List[str] = []
    slug: str = ""
    params: str = ""
    query: str = ""
    fragment: str = ""
