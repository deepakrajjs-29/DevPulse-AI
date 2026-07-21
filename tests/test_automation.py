"""
Unit tests for DevPulse AI ChangeDetector automation module.
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from devpulse.automation.change_detector import ChangeDetector


class TestChangeDetector(unittest.TestCase):
    """Test suite verifying SHA-256 hashing and change detection scan logic."""

    def setUp(self):
        self.detector = ChangeDetector()

    def test_compute_hash(self):
        """Verify SHA-256 hash output string generation."""
        h1 = self.detector.compute_hash("hello world")
        h2 = self.detector.compute_hash("hello world")
        h3 = self.detector.compute_hash("different text")

        self.assertEqual(len(h1), 64)
        self.assertEqual(h1, h2)
        self.assertNotEqual(h1, h3)

    def test_has_changed_non_existent_file(self):
        """Verify non-existent file returns True (change detected)."""
        with TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "missing.txt"
            self.assertTrue(self.detector.has_changed(file_path, "new content"))

    def test_has_changed_existing_file(self):
        """Verify identical content returns False and modified content returns True."""
        with TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "test.txt"
            file_path.write_text("initial content", encoding="utf-8")

            # Same content -> False
            self.assertFalse(self.detector.has_changed(file_path, "initial content"))

            # Modified content -> True
            self.assertTrue(self.detector.has_changed(file_path, "updated content"))

    def test_detect_changes_batch(self):
        """Verify batch change detection scan across multiple files."""
        with TemporaryDirectory() as tmp_dir:
            f1 = Path(tmp_dir) / "file1.txt"
            f2 = Path(tmp_dir) / "file2.txt"

            f1.write_text("unchanged content", encoding="utf-8")
            f2.write_text("old content", encoding="utf-8")

            content_map = {
                f1: "unchanged content",
                f2: "new content",
            }

            changed = self.detector.detect_changes(content_map)
            self.assertEqual(len(changed), 1)
            self.assertIn(f2, changed)


if __name__ == "__main__":
    unittest.main()
