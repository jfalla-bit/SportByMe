from typing import List, Optional
from ..domain.entities.tournament import Tournament
from ..domain.repositories.tournament_repository import TournamentRepository
from .models.tournament_model import TournamentModel

class TournamentRepositoryImpl(TournamentRepository):
    def save(self, tournament: Tournament) -> Tournament:
        if tournament.id:
            tournament_model = TournamentModel.objects.get(id=tournament.id)
            tournament_model.name = tournament.name
            tournament_model.start_date = tournament.start_date
            tournament_model.end_date = tournament.end_date
            tournament_model.category_id = tournament.category_id
            tournament_model.is_active = tournament.is_active
        else:
            tournament_model = TournamentModel(
                name=tournament.name,
                start_date=tournament.start_date,
                end_date=tournament.end_date,
                category_id=tournament.category_id,
                is_active=tournament.is_active
            )
        
        tournament_model.save()
        return self._to_entity(tournament_model)
    
    def find_by_id(self, tournament_id: int) -> Optional[Tournament]:
        try:
            tournament_model = TournamentModel.objects.get(id=tournament_id)
            return self._to_entity(tournament_model)
        except TournamentModel.DoesNotExist:
            return None
    
    def find_all(self) -> List[Tournament]:
        tournaments = TournamentModel.objects.all()
        return [self._to_entity(t) for t in tournaments]
    
    def find_active(self) -> List[Tournament]:
        tournaments = TournamentModel.objects.filter(is_active=True)
        return [self._to_entity(t) for t in tournaments]
    
    def delete(self, tournament_id: int) -> bool:
        try:
            TournamentModel.objects.get(id=tournament_id).delete()
            return True
        except TournamentModel.DoesNotExist:
            return False
    
    def _to_entity(self, model: TournamentModel) -> Tournament:
        return Tournament(
            id=model.id,
            name=model.name,
            start_date=model.start_date,
            end_date=model.end_date,
            category_id=model.category_id,
            is_active=model.is_active
        )