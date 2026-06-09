from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.training import Training

class TrainingRepository(ABC):
    @abstractmethod
    def save(self, training: Training) -> Training:
        pass
    
    @abstractmethod
    def find_by_id(self, training_id: int) -> Optional[Training]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Training]:
        pass
    
    @abstractmethod
    def find_by_team(self, team_id: int) -> List[Training]:
        pass
    
    @abstractmethod
    def delete(self, training_id: int) -> bool:
        pass