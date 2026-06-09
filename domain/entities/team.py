from dataclasses import dataclass
from typing import Optional

@dataclass
class Team:
    id: Optional[int]
    name: str
    category_id: int
    coach_id: Optional[int]
    is_active: bool = True