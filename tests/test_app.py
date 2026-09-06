import json
import tempfile
import unittest
from pathlib import Path

from app import add_task, complete_task, load_tasks


class TaskTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "tasks.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_task_assigns_next_id(self):
        add_task("Первая задача", self.path)
        task = add_task("Вторая задача", self.path)

        self.assertEqual(task["id"], 2)
        self.assertEqual(len(load_tasks(self.path)), 2)

    def test_complete_task_marks_existing_task(self):
        add_task("Проверить тесты", self.path)

        result = complete_task(1, self.path)

        self.assertTrue(result["done"])
        self.assertTrue(load_tasks(self.path)[0]["done"])

    def test_complete_task_returns_none_for_unknown_id(self):
        self.path.write_text(json.dumps([]), encoding="utf-8")

        self.assertIsNone(complete_task(99, self.path))


if __name__ == "__main__":
    unittest.main()
