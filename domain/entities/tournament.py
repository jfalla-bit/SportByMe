from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Tournament:
    id: Optional[int]
    name: str
    start_date: date
    end_date: date
    category_id: int
    is_active: bool = True