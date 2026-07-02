

from typing import Optional

from ..repositories.task_repository import TaskRepository
from ..domain.models import Task, TaskStatus
from ..config import DB_PATH

class TaskService:
 

    def __init__(self, db_path=DB_PATH) -> None:

        self._repo = TaskRepository(db_path)

    def create_task(self, title: str, description: str = "", user_id: int = None) -> Task:
    
        if not title or not title.strip():
            raise ValueError("O título da tarefa é obrigatório.")

        if len(title.strip()) < 3:
            raise ValueError("O título deve ter pelo menos 3 caracteres.")

        if user_id is None:
            raise ValueError("user_id é obrigatório para criar uma tarefa.")

        task = Task(title=title, description=description, user_id=user_id)
        return self._repo.create(task)

    def get_all(self) -> list[Task]:

        return self._repo.find_all()

    def get_pending(self) -> list[Task]:

        all_tasks = self._repo.find_all()
        return list(filter(lambda t: t.status != TaskStatus.DONE, all_tasks))

    def get_summary(self) -> dict:
        

        counts = self._repo.count_by_status()
        total = self._repo.count()

        return {
            "total":       total,
            "todo":        counts.get("todo", 0),
            "in_progress": counts.get("in_progress", 0),
            "done":        counts.get("done", 0),
        }

    def start_task(self, task_id: int) -> Task:
   

        return self._change_status(task_id, TaskStatus.IN_PROGRESS)

    def complete_task(self, task_id: int) -> Task:
       

        return self._change_status(task_id, TaskStatus.DONE)

    def delete_task(self, task_id: int) -> None:


        task = self._repo.find_by_id(task_id)
        if task is None:
            raise ValueError(f"Tarefa #{task_id} não encontrada.")

        self._repo.delete(task_id)

    def get_titles(self) -> list[str]:

        return list(map(lambda t: t.title, self.get_all()))
 
    def _change_status(self, task_id: int, new_status: TaskStatus) -> Task:
      

        task = self._repo.find_by_id(task_id)
        if task is None:
            raise ValueError(f"Tarefa #{task_id} não encontrada.")

        task.status = new_status
        self._repo.update(task)
        return task