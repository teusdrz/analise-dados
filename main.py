from src.database import create_tables
from src.service import TaskService
from src.user_repository import UserRepository
from src.models import User




def print_header(title: str) -> None:
    
    print(f"\n{'_'* 40}")
    print(f"  {title}")
    print(f"{'_'* 40}")
    
def print_menu() -> None:
    
    print("\nMenu:")
    print("1. Listar tarefa")
    print("2. Criar tarefas")
    print("3. Iniciar tarefas")
    print("4. Concluir tarefa")
    print("5. Deletar tarefa")
    print("6. Resumo tarefa")
    print("0. Sair")
    print()
    
def list_tasks(service: TaskService) -> None:
    tasks = service.get_all()
    print_header("TAREFAS")
    if not tasks:
        print("  Nenhuma tarefa cadastrada.")
        return
    for task in tasks:
        print(f"  {task}")
    

def create_task(service: TaskService, user_id: int) -> None:
    print_header("Criar Tarefa")
    title = input(" Título: ").strip()
    description = input(" Descrição (opcional): ").strip()
    try:
        task = service.create_task(title, description, user_id=user_id)
        print(f"Tarefa criada com sucesso: #{task.id}")
    except ValueError as e:
        print(f"Erro ao criar tarefa: {e}")
        




def change_task_status(service: TaskService, action: str) -> None:
   
    print_header(f"{'INICIAR' if action == 'start' else 'CONCLUIR'} TAREFA")
    try:
        task_id = int(input("  ID da tarefa: "))
        if action == "start":
            task = service.start_task(task_id)
        else:
            task = service.complete_task(task_id)
        print(f"\n   {task}")
    except ValueError as e:
        print(f"\n   Erro: {e}")
        
def delete_task(service: TaskService) -> None:
    print_header("Deletar Tarefa")
    try:
        task_id = int(input(" ID da tarefa:"))
        service.delete_task(task_id)
        print(f"Tarefa #{task_id} deletada com sucesso.")
    except ValueError as e:
        print(f"\n   Erro: {e}")
        
def show_summary(service: TaskService) -> None:
    summary = service.get_summary()
    print_header("Resumo de Tarefas")
    print(f"Total:        {summary['total']}")
    print(f"To Do:        {summary['todo']}")
    print(f"In Progress:  {summary['in_progress']}")
    print(f"Done:         {summary['done']}")
    
    
         
def get_or_create_default_user(user_repo: UserRepository) -> User:
    user = user_repo.find_by_email("dev@local")
    if user is None:
        user = user_repo.create(User(name="Usuário Padrão", email="dev@local"))
    return user
    
def main() -> None:

    create_tables()
    service = TaskService()
    user_repo = UserRepository()
    current_user = get_or_create_default_user(user_repo)

    while True:
        print_menu()
        choice = input("Escolha uma opção: ").strip()

        match choice:
            case "1": list_tasks(service)
            case "2": create_task(service, current_user.id)
            case "3": change_task_status(service, "start")
            case "4": change_task_status(service, "complete")
            case "5": delete_task(service)
            case "6": show_summary(service)
            case "0":
                print("\n  Até logo!\n")
                break
            case _:
                print("\n  Opção inválida.")


if __name__ == "__main__":
    main()