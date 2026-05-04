from pydantic import BaseModel, UUID4
from datetime import datetime

class FollowUserRequest(BaseModel):
    following_id: UUID4

class UnfollowUserRequest(BaseModel):
    following_id: UUID4

class FollowResponse(BaseModel):
    follower_id: UUID4
    following_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True  

class FollowListResponse(BaseModel):
    followed_users: list[UUID4]

class FollowStatusResponse(BaseModel):
    is_followed: bool