import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: uuid.UUID
    display_name: str
    username: str
    email: Optional[EmailStr] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}