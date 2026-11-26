from hashlib import scrypt
from hmac import compare_digest
from secrets import token_bytes
from uuid import UUID, uuid4

from fastapi import HTTPException

from app.models.users import User
from app.schemas.users import UserSignIn, UserCredentials, UserRole
from app.storage.memory import find_user, get_user, save_user


def hash_password(password: str, salt: bytes) -> bytes:
    return scrypt(password.encode(), salt=salt, n=16384, r=8, p=1)


def signup(data: UserCredentials) -> User:
    if find_user(data.username):
        raise HTTPException(409, "Username already exists")
    salt = token_bytes(16)
    return save_user(User(uuid4(), data.username, hash_password(data.password, salt), salt))


def signin(data: UserSignIn) -> User:
    user = find_user(data.username)
    if user is None or not compare_digest(hash_password(data.password, user.salt), user.password_hash):
        raise HTTPException(401, "Invalid username or password")
    return user


def update_role(user_id: UUID, role: UserRole) -> User:
    user = get_user(user_id)
    if user is None:
        raise HTTPException(404, "User not found")
    user.role = role
    return save_user(user)
