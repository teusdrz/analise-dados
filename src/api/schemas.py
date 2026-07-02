

from datetime import datetime
from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):

    title: str = Field(..., min_length=3, description="Título da tarefa")
    description: str = Field(default="", description="Descrição opcional")
    user_id: int = Field(..., description="ID do usuário dono da tarefa")



class TaskResponse(BaseModel):
 

    id: int
    title: str
    description: str
    status: str
    created_at: datetime
    user_id: int

    class Config:
        
        from_attributes = True


class TaskSummaryResponse(BaseModel):

    total: int
    todo: int
    in_progress: int
    done: int


class ErrorResponse(BaseModel):

    detail: str