import unittest
import os
import json
import tempfile
import task_app


class TestTaskApp(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.tmp.close()
        task_app.DATA_FILE = self.tmp.name

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_add_task(self):
        task_app.add_task('Тестовая задача')
        with open(self.tmp.name, encoding='utf-8') as f:
            tasks = json.load(f)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['title'], 'Тестовая задача')


if __name__ == '__main__':
    unittest.main()
class TestAddTaskPriority(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.tmp.close()
        task_app.DATA_FILE = self.tmp.name

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_add_with_priority(self):
        task_app.add_task('Срочная', priority='high')
        with open(self.tmp.name, encoding='utf-8') as f:
            tasks = json.load(f)
        self.assertEqual(tasks[0]['priority'], 'high')

class TestCompleteTask(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.tmp.close()
        task_app.DATA_FILE = self.tmp.name
        task_app.add_task('Задача для выполнения')

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_complete(self):
        task_app.complete_task(1)
        with open(self.tmp.name, encoding='utf-8') as f:
            tasks = json.load(f)
        self.assertEqual(tasks[0]['status'], 'done')

class TestFilterByStatus(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.tmp.close()
        task_app.DATA_FILE = self.tmp.name
        task_app.add_task('Открытая')
        task_app.add_task('Закрытая')
        task_app.complete_task(2)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_filter_open(self):
        tasks = task_app.load_tasks()
        opened = [t for t in tasks if t['status'] == 'open']
        self.assertEqual(len(opened), 1)
        self.assertEqual(opened[0]['title'], 'Открытая')
