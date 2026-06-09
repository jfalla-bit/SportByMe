from typing import List, Optional
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository

class UserUseCases:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def create_user(self, user: User) -> User:
        return self.user_repository.save(user)
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repository.find_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.user_repository.find_by_username(username)
    
    def get_all_users(self) -> List[User]:
        return self.user_repository.find_all()
    
    def get_users_by_role(self, role: str) -> List[User]:
        return self.user_repository.find_by_role(role)
    
    def update_user(self, user: User) -> User:
        return self.user_repository.save(user)
    
    def delete_user(self, user_id: int) -> bool:
        return self.user_repository.delete(user_id)
    
    # Métodos de compatibilidad con código existente
    def list_users(self):
        return self.get_all_users()
    
    def create_user_legacy(self, name, email, role):
        user = User(None, name, email, '', '', role)
        return self.create_user(user)