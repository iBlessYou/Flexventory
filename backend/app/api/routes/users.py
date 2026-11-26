from uuid import UUID

from fastapi import APIRouter

from app.schemas.users import UserSignIn, UserCredentials, UserResponse, UserRoleUpdate
from app.services import users

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup(data: UserCredentials):
    return users.signup(data)


@router.post("/signin", response_model=UserResponse)
async def signin(data: UserSignIn):
    return users.signin(data)


@router.patch("/{user_id}/role", response_model=UserResponse)
async def update_role(user_id: UUID, data: UserRoleUpdate):
    return users.update_role(user_id, data.role)
