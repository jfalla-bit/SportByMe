from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Training:
    id: Optional[int]
    team_id: int
    date: datetime
    duration_minutes: int
    description: str
    location: str