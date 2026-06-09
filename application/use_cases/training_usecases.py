from typing import List, Optional
from ..domain.entities.training import Training
from ..domain.repositories.training_repository import TrainingRepository

class TrainingUseCases:
    def __init__(self, training_repository: TrainingRepository):
        self.training_repository = training_repository
    
    def create_training(self, training: Training) -> Training:
        return self.training_repository.save(training)
    
    def get_training(self, training_id: int) -> Optional[Training]:
        return self.training_repository.find_by_id(training_id)
    
    def get_all_trainings(self) -> List[Training]:
        return self.training_repository.find_all()
    
    def get_trainings_by_team(self, team_id: int) -> List[Training]:
        return self.training_repository.find_by_team(team_id)
    
    def update_training(self, training: Training) -> Training:
        return self.training_repository.save(training)
    
    def delete_training(self, training_id: int) -> bool:
        return self.training_repository.delete(training_id)