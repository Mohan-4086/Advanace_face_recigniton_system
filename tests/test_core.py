import csv
import importlib
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from auth import hash_password, verify_password
from student_metadata import read_student


class CoreTests(unittest.TestCase):
    def test_passwords_are_salted_and_verify(self):
        password = "a password with spaces "
        first, second = hash_password(password), hash_password(password)
        self.assertNotEqual(first, second)
        self.assertTrue(verify_password(password, first))
        self.assertFalse(verify_password(password.strip(), first))
        self.assertFalse(verify_password(password, "malformed"))

    def test_metadata_keeps_full_name_and_teacher(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            expected = {"name": "Alex Kumar Singh", "teacher": "teacher_one", "created": "2026-09-07"}
            (folder / "student.json").write_text(json.dumps(expected))
            self.assertEqual(read_student(folder), expected)

    def test_csv_quoting_duplicates_and_distinct_students(self):
        with tempfile.TemporaryDirectory() as directory:
            config = types.ModuleType("config")
            config.ATTENDANCE_DIR = directory
            # Core persistence tests do not require pandas or a desktop.
            pandas = types.ModuleType("pandas")
            with patch.dict(sys.modules, {"config": config, "pandas": pandas}):
                sys.modules.pop("attendance", None)
                attendance = importlib.import_module("attendance")
                self.assertTrue(attendance.mark_attendance("Alex, Singh", "teacher_one", "id1"))
                self.assertFalse(attendance.mark_attendance("Alex, Singh", "teacher_one", "id1"))
                attendance = importlib.reload(attendance)
                self.assertFalse(attendance.mark_attendance("Alex, Singh", "teacher_one", "id1"))
                self.assertTrue(attendance.mark_attendance("Alex, Singh", "teacher_one", "id2"))
                self.assertTrue(attendance.mark_attendance("Alex, Singh", "teacher_two", "id1"))
                with open(attendance.get_attendance_file(), newline="") as file:
                    rows = list(csv.DictReader(file))
                self.assertEqual(len(rows), 3)
                self.assertEqual(rows[0]["Name"], "Alex, Singh")
            sys.modules.pop("attendance", None)


if __name__ == "__main__":
    unittest.main()
