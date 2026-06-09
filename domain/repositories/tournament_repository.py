from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.tournament import Tournament

class TournamentRepository(ABC):
    @abstractmethod
    def save(self, tournament: Tournament) -> Tournament:
        pass
    
    @abstractmethod
    def find_by_id(self, tournament_id: int) -> Optional[Tournament]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Tournament]:
        pass
    
    @abstractmethod
    def find_active(self) -> List[Tournament]:
        pass
    
    @abstractmethod
    def delete(self, tournament_id: int) -> bool:
        pass