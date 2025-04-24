import unittest
from app.priorities.emerg_priority import Priority

class TestPriority(unittest.TestCase):
    def test_priority_enum_values(self):
        """Test that the Priority enum contains the correct values."""
        self.assertEqual(Priority.HIGH.value, "high")
        self.assertEqual(Priority.MEDIUM.value, "medium")
        self.assertEqual(Priority.LOW.value, "low")

    def test_priority_enum_members(self):
        """Test that the Priority enum contains the correct members."""
        self.assertIn("HIGH", Priority.__members__)
        self.assertIn("MEDIUM", Priority.__members__)
        self.assertIn("LOW", Priority.__members__)

    def test_priority_enum_case_insensitivity(self):
        """Test that Priority enum can be accessed in a case-insensitive manner."""
        self.assertEqual(Priority["HIGH"], Priority.HIGH)
        self.assertEqual(Priority["high".upper()], Priority.HIGH)

    def test_priority_enum_string_representation(self):
        """Test the string representation of Priority enum members."""
        self.assertEqual(str(Priority.HIGH), "high")
        self.assertEqual(str(Priority.MEDIUM), "medium")
        self.assertEqual(str(Priority.LOW), "low")

if __name__ == "__main__":
    unittest.main()