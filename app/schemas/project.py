from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    manager_id: int

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    class Config:
        from_attributes = True