from typing import List, Optional
from ..domain.entities.training import Training
from ..domain.repositories.training_repository import TrainingRepository
from .models.training_model import TrainingModel

class TrainingRepositoryImpl(TrainingRepository):
    def save(self, training: Training) -> Training:
        if training.id:
            training_model = TrainingModel.objects.get(id=training.id)
            training_model.team_id = training.team_id
            training_model.date = training.date
            training_model.duration_minutes = training.duration_minutes
            training_model.description = training.description
            training_model.location = training.location
        else:
            training_model = TrainingModel(
                team_id=training.team_id,
                date=training.date,
                duration_minutes=training.duration_minutes,
                description=training.description,
                location=training.location
            )
        
        training_model.save()
        return self._to_entity(training_model)
    
    def find_by_id(self, training_id: int) -> Optional[Training]:
        try:
            training_model = TrainingModel.objects.get(id=training_id)
            return self._to_entity(training_model)
        except TrainingModel.DoesNotExist:
            return None
    
    def find_all(self) -> List[Training]:
        trainings = TrainingModel.objects.all()
        return [self._to_entity(t) for t in trainings]
    
    def find_by_team(self, team_id: int) -> List[Training]:
        trainings = TrainingModel.objects.filter(team_id=team_id)
        return [self._to_entity(t) for t in trainings]
    
    def delete(self, training_id: int) -> bool:
        try:
            TrainingModel.objects.get(id=training_id).delete()
            return True
        except TrainingModel.DoesNotExist:
            return False
    
    def _to_entity(self, model: TrainingModel) -> Training:
        return Training(
            id=model.id,
            team_id=model.team_id,
            date=model.date,
            duration_minutes=model.duration_minutes,
            description=model.description,
            location=model.location
        )