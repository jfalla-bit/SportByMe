from dataclasses import dataclass
from typing import Optional

@dataclass
class Category:
    id: Optional[int]
    name: str
    min_age: int
    max_age: int
    is_active: bool = True