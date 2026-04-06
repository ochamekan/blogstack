from pydantic import ValidationError
from src.auth.exceptions import EmailAlreadyTaken
from src.auth.models import User
from src.auth.repository import AuthRepository
from src.auth.schemes import CreateUserRequest
from src.security.utils import hash_password


class AuthService:
    def __init__(self, repo: AuthRepository):
        self._repo: AuthRepository = repo

    def signup(self, data: CreateUserRequest) -> User:
        if self._repo.get_user_by_email(data.email):
            raise EmailAlreadyTaken("Email already taken")

        try:
            user = User.model_validate(
                data, update={"hashed_password": hash_password(data.password)}
            )
        except ValidationError:
            raise

        new_user = self._repo.create_user(user)

        return new_user
