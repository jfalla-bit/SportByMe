from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from application.use_cases.tournament_usecases import TournamentUseCases
from infrastructure.repositories.tournament_repository_impl import TournamentRepositoryImpl

tournament_use_cases = TournamentUseCases(TournamentRepositoryImpl())

@api_view(['GET', 'POST'])
def tournament_list(request):
    if request.method == 'GET':
        tournaments = tournament_use_cases.get_all_tournaments()
        return Response([{
            'id': t.id,
            'name': t.name,
            'start_date': t.start_date,
            'end_date': t.end_date,
            'category_id': t.category_id,
            'is_active': t.is_active
        } for t in tournaments])
    
    elif request.method == 'POST':
        # Implementar creación de torneo
        pass

@api_view(['GET', 'PUT', 'DELETE'])
def tournament_detail(request, pk):
    tournament = tournament_use_cases.get_tournament(pk)
    if not tournament:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response({
            'id': tournament.id,
            'name': tournament.name,
            'start_date': tournament.start_date,
            'end_date': tournament.end_date,
            'category_id': tournament.category_id,
            'is_active': tournament.is_active
        })
    
    elif request.method == 'PUT':
        # Implementar actualización
        pass
    
    elif request.method == 'DELETE':
        tournament_use_cases.delete_tournament(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)