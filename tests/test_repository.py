

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import create_tables
from src.models import Task, TaskStatus
from src.repository import TaskRepository
from src.service import TaskService


class TestTaskRepository(unittest.TestCase):

    def setUp(self) -> None:
      
        self.db_fd, self.db_path_str = tempfile.mkstemp(suffix=".db")
        self.db_path = Path(self.db_path_str)
        create_tables(self.db_path)
        self.repo = TaskRepository(self.db_path)

    def tearDown(self) -> None:
        os.close(self.db_fd)
        os.unlink(self.db_path_str)

  

    def test_create_returns_task_with_id(self) -> None:
        task = self.repo.create(Task(title="Estudar Python", description=""))
        self.assertIsNotNone(task.id)
        self.assertIsInstance(task.id, int)

    def test_create_default_status_is_todo(self) -> None:
        task = self.repo.create(Task(title="Nova tarefa", description=""))
        self.assertEqual(task.status, TaskStatus.TODO)

  
    def test_find_all_returns_empty_when_no_tasks(self) -> None:
        result = self.repo.find_all()
        self.assertEqual(result, [])

    def test_find_all_returns_all_created_tasks(self) -> None:
        self.repo.create(Task(title="Tarefa Um", description=""))
        self.repo.create(Task(title="Tarefa Dois", description=""))
        result = self.repo.find_all()
        self.assertEqual(len(result), 2)

    def test_find_by_id_returns_correct_task(self) -> None:
        created = self.repo.create(Task(title="Minha tarefa", description="Desc"))
        found = self.repo.find_by_id(created.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "Minha tarefa")

    def test_find_by_id_returns_none_when_not_found(self) -> None:
        result = self.repo.find_by_id(999)
        self.assertIsNone(result)

    def test_find_by_status_filters_correctly(self) -> None:
        t1 = self.repo.create(Task(title="Pendente", description=""))
        t2 = self.repo.create(Task(title="Concluída", description=""))
        t2.status = TaskStatus.DONE
        self.repo.update(t2)

        pending = self.repo.find_by_status(TaskStatus.TODO)
        done    = self.repo.find_by_status(TaskStatus.DONE)

        self.assertEqual(len(pending), 1)
        self.assertEqual(len(done), 1)
        self.assertEqual(pending[0].title, "Pendente")

   

    def test_update_changes_status(self) -> None:
        task = self.repo.create(Task(title="Tarefa", description=""))
        task.status = TaskStatus.DONE
        updated = self.repo.update(task)
        self.assertTrue(updated)

        found = self.repo.find_by_id(task.id)
        self.assertEqual(found.status, TaskStatus.DONE)

    def test_update_returns_false_for_nonexistent_id(self) -> None:
        fake_task = Task(title="Fake", description="", id=999)
        result = self.repo.update(fake_task)
        self.assertFalse(result)

   
    def test_delete_removes_task(self) -> None:
        task = self.repo.create(Task(title="Para deletar", description=""))
        deleted = self.repo.delete(task.id)
        self.assertTrue(deleted)
        self.assertIsNone(self.repo.find_by_id(task.id))

    def test_delete_returns_false_for_nonexistent_id(self) -> None:
        result = self.repo.delete(999)
        self.assertFalse(result)

 
    def test_count_returns_correct_number(self) -> None:
        self.assertEqual(self.repo.count(), 0)
        self.repo.create(Task(title="Um", description=""))
        self.repo.create(Task(title="Dois", description=""))
        self.assertEqual(self.repo.count(), 2)

    def test_count_by_status(self) -> None:
        t1 = self.repo.create(Task(title="Pendente", description=""))
        t2 = self.repo.create(Task(title="Concluída", description=""))
        t2.status = TaskStatus.DONE
        self.repo.update(t2)

        counts = self.repo.count_by_status()
        self.assertEqual(counts.get("todo"), 1)
        self.assertEqual(counts.get("done"), 1)


class TestTaskService(unittest.TestCase):

    def setUp(self) -> None:
        self.db_fd, self.db_path_str = tempfile.mkstemp(suffix=".db")
        self.db_path = Path(self.db_path_str)
        create_tables(self.db_path)
        self.service = TaskService(self.db_path)

    def tearDown(self) -> None:
        os.close(self.db_fd)
        os.unlink(self.db_path_str)

    def test_create_task_validates_empty_title(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create_task("")

    def test_create_task_validates_short_title(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create_task("AB")

    def test_complete_task_changes_status(self) -> None:
        task = self.service.create_task("Estudar SQL")
        completed = self.service.complete_task(task.id)
        self.assertTrue(completed.is_done)

    def test_complete_nonexistent_task_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            self.service.complete_task(999)

    def test_get_pending_excludes_done_tasks(self) -> None:
        t1 = self.service.create_task("Pendente")
        t2 = self.service.create_task("Concluída")
        self.service.complete_task(t2.id)

        pending = self.service.get_pending()
        titles  = [t.title for t in pending]

        self.assertIn("Pendente", titles)
        self.assertNotIn("Concluída", titles)

    def test_get_summary_counts_correctly(self) -> None:
        self.service.create_task("Tarefa Um")
        t2 = self.service.create_task("Tarefa Dois")
        self.service.complete_task(t2.id)

        summary = self.service.get_summary()
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["todo"], 1)
        self.assertEqual(summary["done"], 1)

    def test_delete_nonexistent_task_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete_task(999)

    def test_get_titles_returns_list_of_strings(self) -> None:
        self.service.create_task("Python")
        self.service.create_task("SQL puro")
        titles = self.service.get_titles()
        self.assertIn("Python", titles)
        self.assertIn("SQL puro", titles)


if __name__ == "__main__":
    unittest.main(verbosity=2)
