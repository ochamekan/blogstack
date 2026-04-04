from src.auth.models import User
from src.auth.repository import AuthRepository
from src.auth.schemes import CreateUserRequest


class AuthService:
    def __init__(self, repo: AuthRepository):
        self._repo: AuthRepository = repo

    def signup(self, data: CreateUserRequest) -> User:
        if self._repo.get_user_by_email(data.email):
            raise Exception("Email already taken")

        user = User.model_validate(data, update={"hashed_password": "somehashedpswrd"})
        return user
