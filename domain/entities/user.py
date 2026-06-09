from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    phone: Optional[str] = None
    birth_date: Optional[date] = None
    is_active: bool = True
    
    def is_administrador(self) -> bool:
        return self.role == 'administrador'
    
    def is_entrenador(self) -> bool:
        return self.role == 'entrenador'
    
    def is_deportista(self) -> bool:
        return self.role == 'deportista'