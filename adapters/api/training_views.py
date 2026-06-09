from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from application.use_cases.training_usecases import TrainingUseCases
from infrastructure.repositories.training_repository_impl import TrainingRepositoryImpl

training_use_cases = TrainingUseCases(TrainingRepositoryImpl())

@api_view(['GET', 'POST'])
def training_list(request):
    if request.method == 'GET':
        trainings = training_use_cases.get_all_trainings()
        return Response([{
            'id': t.id,
            'team_id': t.team_id,
            'date': t.date,
            'duration_minutes': t.duration_minutes,
            'description': t.description,
            'location': t.location
        } for t in trainings])
    
    elif request.method == 'POST':
        # Implementar creación de entrenamiento
        pass

@api_view(['GET', 'PUT', 'DELETE'])
def training_detail(request, pk):
    training = training_use_cases.get_training(pk)
    if not training:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response({
            'id': training.id,
            'team_id': training.team_id,
            'date': training.date,
            'duration_minutes': training.duration_minutes,
            'description': training.description,
            'location': training.location
        })
    
    elif request.method == 'PUT':
        # Implementar actualización
        pass
    
    elif request.method == 'DELETE':
        training_use_cases.delete_training(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)