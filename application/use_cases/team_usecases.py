from typing import List, Optional
from ..domain.entities.team import Team
from ..domain.repositories.team_repository import TeamRepository

class TeamUseCases:
    def __init__(self, team_repository: TeamRepository):
        self.team_repository = team_repository
    
    def create_team(self, team: Team) -> Team:
        return self.team_repository.save(team)
    
    def get_team(self, team_id: int) -> Optional[Team]:
        return self.team_repository.find_by_id(team_id)
    
    def get_all_teams(self) -> List[Team]:
        return self.team_repository.find_all()
    
    def get_teams_by_category(self, category_id: int) -> List[Team]:
        return self.team_repository.find_by_category(category_id)
    
    def update_team(self, team: Team) -> Team:
        return self.team_repository.save(team)
    
    def delete_team(self, team_id: int) -> bool:
        return self.team_repository.delete(team_id)