from sqlmodel import Session, select

from src.auth.models import User


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self._db: Session = db

    def get_user_by_email(self, email: str) -> User | None:
        return self._db.exec(select(User).where(User.email == email)).first()

    def create_user(self, new_user: User) -> User:
        self._db.add(new_user)
        self._db.commit()
        return new_user
