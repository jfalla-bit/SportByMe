from typing import List, Optional
from ..domain.entities.tournament import Tournament
from ..domain.repositories.tournament_repository import TournamentRepository

class TournamentUseCases:
    def __init__(self, tournament_repository: TournamentRepository):
        self.tournament_repository = tournament_repository
    
    def create_tournament(self, tournament: Tournament) -> Tournament:
        return self.tournament_repository.save(tournament)
    
    def get_tournament(self, tournament_id: int) -> Optional[Tournament]:
        return self.tournament_repository.find_by_id(tournament_id)
    
    def get_all_tournaments(self) -> List[Tournament]:
        return self.tournament_repository.find_all()
    
    def get_active_tournaments(self) -> List[Tournament]:
        return self.tournament_repository.find_active()
    
    def update_tournament(self, tournament: Tournament) -> Tournament:
        return self.tournament_repository.save(tournament)
    
    def delete_tournament(self, tournament_id: int) -> bool:
        return self.tournament_repository.delete(tournament_id)