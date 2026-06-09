from typing import List, Optional
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from core.models import UserModel

class UserRepositoryImpl(UserRepository):
    def save(self, user: User) -> User:
        if user.id:
            user_model = UserModel.objects.get(id=user.id)
            user_model.username = user.username
            user_model.email = user.email
            user_model.first_name = user.first_name
            user_model.last_name = user.last_name
            user_model.role = user.role
            user_model.phone = user.phone
            user_model.birth_date = user.birth_date
            user_model.is_active = user.is_active
        else:
            user_model = UserModel(
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                role=user.role,
                phone=user.phone,
                birth_date=user.birth_date,
                is_active=user.is_active
            )
        
        user_model.save()
        return self._to_entity(user_model)
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        try:
            user_model = UserModel.objects.get(id=user_id)
            return self._to_entity(user_model)
        except UserModel.DoesNotExist:
            return None
    
    def find_by_username(self, username: str) -> Optional[User]:
        try:
            user_model = UserModel.objects.get(username=username)
            return self._to_entity(user_model)
        except UserModel.DoesNotExist:
            return None
    
    def find_all(self) -> List[User]:
        users = UserModel.objects.all()
        return [self._to_entity(u) for u in users]
    
    def find_by_role(self, role: str) -> List[User]:
        users = UserModel.objects.filter(role=role)
        return [self._to_entity(u) for u in users]
    
    def delete(self, user_id: int) -> bool:
        try:
            UserModel.objects.get(id=user_id).delete()
            return True
        except UserModel.DoesNotExist:
            return False
    
    def get_all(self):
        return UserModel.objects.all()
    
    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            role=model.role,
            phone=model.phone,
            birth_date=model.birth_date,
            is_active=model.is_active
        )