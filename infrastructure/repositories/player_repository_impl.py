from typing import List, Optional
from ..domain.entities.player import Player
from ..domain.repositories.player_repository import PlayerRepository
from .models.player_model import PlayerModel

class PlayerRepositoryImpl(PlayerRepository):
    def save(self, player: Player) -> Player:
        if player.id:
            player_model = PlayerModel.objects.get(id=player.id)
            player_model.name = player.name
            player_model.last_name = player.last_name
            player_model.birth_date = player.birth_date
            player_model.position = player.position
            player_model.team_id = player.team_id
            player_model.category_id = player.category_id
            player_model.is_active = player.is_active
        else:
            player_model = PlayerModel(
                name=player.name,
                last_name=player.last_name,
                birth_date=player.birth_date,
                position=player.position,
                team_id=player.team_id,
                category_id=player.category_id,
                is_active=player.is_active
            )
        
        player_model.save()
        return self._to_entity(player_model)
    
    def find_by_id(self, player_id: int) -> Optional[Player]:
        try:
            player_model = PlayerModel.objects.get(id=player_id)
            return self._to_entity(player_model)
        except PlayerModel.DoesNotExist:
            return None
    
    def find_all(self) -> List[Player]:
        players = PlayerModel.objects.all()
        return [self._to_entity(p) for p in players]
    
    def find_by_team(self, team_id: int) -> List[Player]:
        players = PlayerModel.objects.filter(team_id=team_id)
        return [self._to_entity(p) for p in players]
    
    def delete(self, player_id: int) -> bool:
        try:
            PlayerModel.objects.get(id=player_id).delete()
            return True
        except PlayerModel.DoesNotExist:
            return False
    
    def _to_entity(self, model: PlayerModel) -> Player:
        return Player(
            id=model.id,
            name=model.name,
            last_name=model.last_name,
            birth_date=model.birth_date,
            position=model.position,
            team_id=model.team_id,
            category_id=model.category_id,
            is_active=model.is_active
        )