
from fastapi import FastAPI

from ..database import create_tables
from ..routes.tasks import router as tasks_router


app = FastAPI(
    title="Task Manager API",
    description="API REST para gerenciamento de tarefas, construída com FastAPI.",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
 
    create_tables()

app.include_router(tasks_router)


@app.get("/")
def health_check():
  
    return {"status": "ok", "service": "task-manager-api"}