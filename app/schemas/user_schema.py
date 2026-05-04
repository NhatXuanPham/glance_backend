from operator import is_
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class MeResponse(BaseModel):
    id: uuid.UUID
    display_name: str
    username: str
    email: Optional[EmailStr] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class UserResponse(BaseModel):
    id: uuid.UUID
    display_name: str
    username: str
    created_at: Optional[datetime] = None
    is_private: bool
    is_following: Optional[bool] = None
    is_follower: Optional[bool] = None
    is_close_friend: Optional[bool] = None
    is_restricted: Optional[bool] = None
    is_blocked_by_me: Optional[bool] = None
    
    model_config = {"from_attributes": True}