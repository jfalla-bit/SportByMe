from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.player import Player

class PlayerRepository(ABC):
    @abstractmethod
    def save(self, player: Player) -> Player:
        pass
    
    @abstractmethod
    def find_by_id(self, player_id: int) -> Optional[Player]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Player]:
        pass
    
    @abstractmethod
    def find_by_team(self, team_id: int) -> List[Player]:
        pass
    
    @abstractmethod
    def delete(self, player_id: int) -> bool:
        pass