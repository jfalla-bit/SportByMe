from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Match:
    id: Optional[int]
    home_team_id: int
    away_team_id: int
    tournament_id: int
    date: datetime
    location: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    status: str = "scheduled"