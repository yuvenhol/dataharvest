from dataclasses import dataclass, field

from typing import List, Optional


@dataclass
class Document:
    url: str
    metadata: dict
    page_content: str


@dataclass
class SearchResultItem:
    title: str
    url: str
    score: Optional[float] = None
    description: str = ""
    content: str = ""


@dataclass
class SearchResult:
    keyword: str
    answer: str
    items: List[SearchResultItem]
    images: List[str] = field(default_factory=list)
