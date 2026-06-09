from typing import List, Optional
from ..domain.entities.player import Player
from ..domain.repositories.player_repository import PlayerRepository

class PlayerUseCases:
    def __init__(self, player_repository: PlayerRepository):
        self.player_repository = player_repository
    
    def create_player(self, player: Player) -> Player:
        return self.player_repository.save(player)
    
    def get_player(self, player_id: int) -> Optional[Player]:
        return self.player_repository.find_by_id(player_id)
    
    def get_all_players(self) -> List[Player]:
        return self.player_repository.find_all()
    
    def get_players_by_team(self, team_id: int) -> List[Player]:
        return self.player_repository.find_by_team(team_id)
    
    def update_player(self, player: Player) -> Player:
        return self.player_repository.save(player)
    
    def delete_player(self, player_id: int) -> bool:
        return self.player_repository.delete(player_id)