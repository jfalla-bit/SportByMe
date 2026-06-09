from typing import List, Optional
from ..domain.entities.team import Team
from ..domain.repositories.team_repository import TeamRepository
from .models.team_model import TeamModel

class TeamRepositoryImpl(TeamRepository):
    def save(self, team: Team) -> Team:
        if team.id:
            team_model = TeamModel.objects.get(id=team.id)
            team_model.name = team.name
            team_model.category_id = team.category_id
            team_model.coach_id = team.coach_id
            team_model.is_active = team.is_active
        else:
            team_model = TeamModel(
                name=team.name,
                category_id=team.category_id,
                coach_id=team.coach_id,
                is_active=team.is_active
            )
        
        team_model.save()
        return self._to_entity(team_model)
    
    def find_by_id(self, team_id: int) -> Optional[Team]:
        try:
            team_model = TeamModel.objects.get(id=team_id)
            return self._to_entity(team_model)
        except TeamModel.DoesNotExist:
            return None
    
    def find_all(self) -> List[Team]:
        teams = TeamModel.objects.all()
        return [self._to_entity(t) for t in teams]
    
    def find_by_category(self, category_id: int) -> List[Team]:
        teams = TeamModel.objects.filter(category_id=category_id)
        return [self._to_entity(t) for t in teams]
    
    def delete(self, team_id: int) -> bool:
        try:
            TeamModel.objects.get(id=team_id).delete()
            return True
        except TeamModel.DoesNotExist:
            return False
    
    def _to_entity(self, model: TeamModel) -> Team:
        return Team(
            id=model.id,
            name=model.name,
            category_id=model.category_id,
            coach_id=model.coach_id,
            is_active=model.is_active
        )