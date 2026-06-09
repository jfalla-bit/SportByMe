from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Player:
    id: Optional[int]
    name: str
    last_name: str
    birth_date: date
    position: str
    team_id: Optional[int]
    category_id: int
    is_active: bool = True