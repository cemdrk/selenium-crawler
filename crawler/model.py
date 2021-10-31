from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Record:
    """Class for dictionary records"""
    title: str
    word_class: str
    definitions: List[str]
    img: Optional[str]
    pronunciations: Optional[List[str]]
