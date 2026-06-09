from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from application.use_cases.team_usecases import TeamUseCases
from infrastructure.repositories.team_repository_impl import TeamRepositoryImpl

team_use_cases = TeamUseCases(TeamRepositoryImpl())

@api_view(['GET', 'POST'])
def team_list(request):
    if request.method == 'GET':
        teams = team_use_cases.get_all_teams()
        return Response([{
            'id': t.id,
            'name': t.name,
            'category_id': t.category_id,
            'coach_id': t.coach_id,
            'is_active': t.is_active
        } for t in teams])
    
    elif request.method == 'POST':
        # Implementar creación de equipo
        pass

@api_view(['GET', 'PUT', 'DELETE'])
def team_detail(request, pk):
    team = team_use_cases.get_team(pk)
    if not team:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response({
            'id': team.id,
            'name': team.name,
            'category_id': team.category_id,
            'coach_id': team.coach_id,
            'is_active': team.is_active
        })
    
    elif request.method == 'PUT':
        # Implementar actualización
        pass
    
    elif request.method == 'DELETE':
        team_use_cases.delete_team(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)