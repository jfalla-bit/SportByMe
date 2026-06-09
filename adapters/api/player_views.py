from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from application.use_cases.player_usecases import PlayerUseCases
from infrastructure.repositories.player_repository_impl import PlayerRepositoryImpl

player_use_cases = PlayerUseCases(PlayerRepositoryImpl())

@api_view(['GET', 'POST'])
def player_list(request):
    if request.method == 'GET':
        players = player_use_cases.get_all_players()
        return Response([{
            'id': p.id,
            'name': p.name,
            'last_name': p.last_name,
            'birth_date': p.birth_date,
            'position': p.position,
            'team_id': p.team_id,
            'category_id': p.category_id,
            'is_active': p.is_active
        } for p in players])
    
    elif request.method == 'POST':
        # Implementar creación de jugador
        pass

@api_view(['GET', 'PUT', 'DELETE'])
def player_detail(request, pk):
    player = player_use_cases.get_player(pk)
    if not player:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response({
            'id': player.id,
            'name': player.name,
            'last_name': player.last_name,
            'birth_date': player.birth_date,
            'position': player.position,
            'team_id': player.team_id,
            'category_id': player.category_id,
            'is_active': player.is_active
        })
    
    elif request.method == 'PUT':
        # Implementar actualización
        pass
    
    elif request.method == 'DELETE':
        player_use_cases.delete_player(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)