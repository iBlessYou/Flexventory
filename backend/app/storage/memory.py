from uuid import UUID

from app.models.users import User

users: dict[UUID, User] = {}


def find_user(username: str) -> User | None:
    return next((user for user in users.values() if user.username.casefold() == username.casefold()), None)


def get_user(user_id: UUID) -> User | None:
    return users.get(user_id)


def save_user(user: User) -> User:
    users[user.id] = user
    return user
