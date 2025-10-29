import unittest
import os

from data_handler import Task,Task_handler,load_tasks_from_file,save_tasks_to_file
from reports import generate_pdf_report

class Test_task_handler(unittest.TestCase):

    def setUp(self):
        self.handler = Task_handler()

    def test_add_task(self):
        task1 = Task(1,"Test Task 1", "Tarea 1", priority=2, status=False, category={"primaria": "Trabajo", "secundaria": ["Urgente"]})
        self.handler.add_task(task1)
        self.assertIn(task1, self.handler.tasks)

    def test_remove_task(self):
        task2 = Task(2,"Test Task 2", "Tarea 2", priority=1, status=True, category={"primaria": "Personal", "secundaria": ["Baja"]})
        self.handler.add_task(task2)
        self.handler.delete_task(task2)
        tasks = self.handler.get_all_tasks()
        self.assertNotIn(task2, tasks)

    def test_get_tasks(self):
        task3 = Task(3,"Test Task 3", "Tarea 3", priority=3, status=False, category={"primaria": "Trabajo", "secundaria": ["Baja"]})
        self.handler.add_task(task3)
        task4 = Task(4,"Test Task 4", "Tarea 4", priority=2, status=True, category={"primaria": "Personal", "secundaria": ["Media"]})
        self.handler.add_task(task4)
        tasks = self.handler.get_all_tasks()
        self.assertEqual(len(tasks), 2)
    
    def test_get_task_by_id(self):
        task1 = Task(6,"Test Task 1", "Tarea 1", priority=2, status=False, category={"primaria": "Trabajo", "secundaria": ["Urgente"]})
        self.handler.add_task(task1)
        found_task = self.handler.get_task_by_id(6)
        self.assertIsNotNone(found_task)
        self.assertEqual(found_task['id'], 6)
        self.assertEqual(found_task['nombre'], "Test Task 1")

    def test_update_task(self):
        task5 = Task(5,"Test Task 5", "Tarea 5", priority=1, status=False, category={"primaria": "Trabajo", "secundaria": ["Urgente"]})
        self.handler.add_task(task5)
        self.handler.update_task(5, name="Updated Task 5", status=True)
        tasks = self.handler.get_all_tasks()
        updated_task = next((t for t in tasks if t['id'] == 5), None)
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task['nombre'], "Updated Task 5")
        self.assertTrue(updated_task['completada'])
    
    def test_complete_task(self):
        task6 = Task(7,"Test Task 6", "Tarea 6", priority=2, status=False, category={"primaria": "Personal", "secundaria": ["Media"]})
        self.handler.add_task(task6)
        self.handler.complete_task(7)
        completed_task = self.handler.get_task_by_id(7)
        self.assertIsNotNone(completed_task)
        self.assertTrue(completed_task['completada'])
    
    def test_change_category(self):
        task = Task(10,"Test Task 10", "Tarea 10", priority=3, status=False, category={"primaria": "Trabajo", "secundaria": ["Baja"]})
        self.handler.add_task(task)
        self.handler.update_task(10, category={"primaria": "Personal", "secundaria": ["Urgente", "Media"]})
        updated_task = self.handler.get_task_by_id(10)
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task['categoria']['primaria'], "Personal")
        self.assertListEqual(updated_task['categoria']['secundaria'], ["Urgente", "Media"])
    
    def test_search_task_by_category(self):
        task_a = Task(11,"Test Task 11", "Tarea 11", priority=2, status=False, category={"primaria": "Trabajo", "secundaria": ["Urgente"]})
        task_b = Task(12,"Test Task 12", "Tarea 12", priority=1, status=True, category={"primaria": "Personal", "secundaria": ["Baja"]})
        self.handler.add_task(task_a)
        self.handler.add_task(task_b)
        trabajo_tasks = self.handler.search_tasks_by_category("Trabajo")
        self.assertEqual(len(trabajo_tasks), 1)
        self.assertEqual(trabajo_tasks[0]['id'], 11)
        personal_tasks = self.handler.search_tasks_by_category("Personal")
        self.assertEqual(len(personal_tasks), 1)
        self.assertEqual(personal_tasks[0]['id'], 12)
        no_tasks = self.handler.search_tasks_by_category("Salud")
        self.assertEqual(len(no_tasks), 0)

    def test_load_tasks(self):
        test_handler = Task_handler()
        task7 = Task(8,"Test Task 7", "Tarea 7", priority=3, status=False, category={"primaria": "Trabajo", "secundaria": ["Baja"]})
        test_handler.add_task(task7)
        save_tasks_to_file(test_handler, 'test_tasks.json')
        new_handler = Task_handler()
        new_handler = load_tasks_from_file('test_tasks.json')
        tasks = new_handler.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['id'], 8)
        self.assertEqual(tasks[0]['nombre'], "Test Task 7")
        os.remove('test_tasks.json')
    
    def test_generate_pdf_report(self):
        pdf_task_manager = Task_handler()
        task8 = Task(9,"Test Task 8", "Tarea 8", priority=1, status=True, category={"primaria": "Personal", "secundaria": ["Urgente"]})
        pdf_task_manager.add_task(task8)
        generate_pdf_report(pdf_task_manager.get_all_tasks(), file_name="test_report.pdf")
        self.assertTrue(os.path.exists('test_report.pdf'))
        os.remove('test_report.pdf')
