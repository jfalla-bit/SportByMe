from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.team import Team

class TeamRepository(ABC):
    @abstractmethod
    def save(self, team: Team) -> Team:
        pass
    
    @abstractmethod
    def find_by_id(self, team_id: int) -> Optional[Team]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Team]:
        pass
    
    @abstractmethod
    def find_by_category(self, category_id: int) -> List[Team]:
        pass
    
    @abstractmethod
    def delete(self, team_id: int) -> bool:
        pass