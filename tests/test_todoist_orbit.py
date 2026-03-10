import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts import todoist_orbit


class CommentInputTests(unittest.TestCase):
    def test_add_comment_inline_rejects_empty_text(self):
        with self.assertRaises(todoist_orbit.TodoistError):
            todoist_orbit.non_empty_text("", source="command line")

    def test_read_comment_content_from_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "note.txt"
            path.write_text("line 1\nline 2\n", encoding="utf-8")
            self.assertEqual(
                todoist_orbit.read_comment_content_from_file(str(path)),
                "line 1\nline 2\n",
            )

    def test_read_comment_content_from_stdin(self):
        with patch("sys.stdin", io.StringIO("hello\nworld\n")):
            self.assertEqual(todoist_orbit.read_comment_content_from_stdin(), "hello\nworld\n")


class ParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = todoist_orbit.configure_parser()

    def test_comments_add_file_parser(self):
        args = self.parser.parse_args(["comments", "add-file", "--task-id", "123", "note.txt"])
        self.assertEqual(args.task_id, "123")
        self.assertEqual(args.file, "note.txt")
        self.assertIs(args.func, todoist_orbit.add_comment_from_file)

    def test_comments_add_stdin_parser(self):
        args = self.parser.parse_args(["comments", "add-stdin", "--project-id", "456"])
        self.assertEqual(args.project_id, "456")
        self.assertIs(args.func, todoist_orbit.add_comment_from_stdin)

    def test_comments_help_mentions_safe_commands(self):
        stdout = io.StringIO()
        with self.assertRaises(SystemExit):
            with redirect_stdout(stdout):
                self.parser.parse_args(["comments", "--help"])
        help_text = stdout.getvalue()
        self.assertIn("add-file", help_text)
        self.assertIn("add-stdin", help_text)


if __name__ == "__main__":
    unittest.main()
