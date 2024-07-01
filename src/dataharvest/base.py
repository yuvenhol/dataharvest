from dataclasses import dataclass


@dataclass
class Document:
    url: str
    metadata: dict
    page_content: str
