from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from application.use_cases.user_usecases import UserUseCases
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from adapters.decorators import admin_required

user_use_cases = UserUseCases(UserRepositoryImpl())

@api_view(['GET', 'POST'])
@admin_required
def user_list(request):
    if request.method == 'GET':
        users = user_use_cases.get_all_users()
        return Response([{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'role': u.role,
            'phone': u.phone,
            'birth_date': u.birth_date,
            'is_active': u.is_active
        } for u in users])
    
    elif request.method == 'POST':
        # Implementar creación de usuario
        pass

@api_view(['GET', 'PUT', 'DELETE'])
@admin_required
def user_detail(request, pk):
    user = user_use_cases.get_user(pk)
    if not user:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'phone': user.phone,
            'birth_date': user.birth_date,
            'is_active': user.is_active
        })
    
    elif request.method == 'PUT':
        # Implementar actualización
        pass
    
    elif request.method == 'DELETE':
        user_use_cases.delete_user(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

# Funciones legacy para compatibilidad
def get_users(request):
    return user_list(request)

def create_user(request):
    return user_list(request)