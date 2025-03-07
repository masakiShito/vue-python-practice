from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union

class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="会議室名")
    capacity: int = Field(..., gt=0, description="収容人数 (1以上)")

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    name: Union[str, None] = Field(None, min_length=1, max_length=50, description="会議室名（変更可能）")
    capacity: Union[int, None] = Field(None, gt=0, description="収容人数 (1以上、変更可能)")

class RoomResponse(RoomBase):
    id: int
    created_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True
