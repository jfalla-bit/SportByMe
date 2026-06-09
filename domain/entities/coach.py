from dataclasses import dataclass
from typing import Optional

@dataclass
class Coach:
    id: Optional[int]
    name: str
    last_name: str
    email: str
    phone: str
    is_active: bool = True