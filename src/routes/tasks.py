

from fastapi import APIRouter, HTTPException

from ..services.task_service import TaskService
from ..api.schemas import TaskCreateRequest, TaskResponse, TaskSummaryResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


service = TaskService()


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(payload: TaskCreateRequest):
   
    try:
        task = service.create_task(
            title=payload.title,
            description=payload.description,
            user_id=payload.user_id,
        )
        return task
    except ValueError as e:
        
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[TaskResponse])
def list_tasks():

    return service.get_all()


@router.get("/summary", response_model=TaskSummaryResponse)
def get_summary():

    return service.get_summary()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):

    task = service._repo.find_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Tarefa #{task_id} não encontrada.")
    return task


@router.patch("/{task_id}/start", response_model=TaskResponse)
def start_task(task_id: int):

    try:
        return service.start_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int):
   

    try:
        return service.complete_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):

    try:
        service.delete_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))