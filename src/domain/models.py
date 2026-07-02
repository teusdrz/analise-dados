from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional



class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

@dataclass
class Task:

     title: str
     description: str
     user_id: int

     id: Optional[int]  = field(default=None)
     status: TaskStatus = field(default=TaskStatus.TODO)
     created_at: datetime = field(default_factory=datetime.now)


     def __post_init__(self) -> None:
                        
        self.title = self.title.strip()
        if not self.title:
           raise ValueError("Title cannot be empty")


        if isinstance(self.status, str):
           self.status = TaskStatus(self.status)
           
     @property
     def status_label(self) -> str:
         
         labels = {
            TaskStatus.TODO: "To Do",
            TaskStatus.IN_PROGRESS: "In Progress",
            TaskStatus.DONE: "Done"
         }

         return labels.get(self.status, self.status.value)
     

     def __str__(self) -> str:
        return f"[{self.id}] {self.title} - {self.status.value}"

@dataclass

class User:
    name: str
    email: str

    id: Optional[int] = field(default=None)

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        self.name = self.name.strip().lower()

        if "@" not in self.email:
            raise ValueError(f"Invalid email address: {self.email}")