import unittest

from linghos.syntax import find_block_end, normalize_script
from linghos.parser import LINGHOSParser


class SyntaxBoundaryTests(unittest.TestCase):
    def test_braces_and_semicolons_inside_strings_are_preserved(self):
        source = 'Main() { Echo("text {; } is literal"); }'
        normalized = normalize_script(source)
        self.assertIn('"text {; } is literal"', normalized)
        lines = normalized.split("\n")
        main_index = next(i for i, line in enumerate(lines) if line.strip() == "Main()")
        self.assertEqual(find_block_end(lines, main_index), len(lines) - 2)

    def test_comments_do_not_affect_block_nesting(self):
        lines = ["Main()", "{", 'Echo("ok"); // }', "}", ""]
        self.assertEqual(find_block_end(lines, 0), 3)

    def test_unclosed_block_returns_none(self):
        self.assertIsNone(find_block_end(["@Start>(PRS_VM)", "{", "ON> x;"], 0))

    def test_interpreter_reports_unclosed_vm_block_without_crashing(self):
        kernel = LINGHOSParser().execute_script("@Start>(PRS_VM) {\nON> target;")
        self.assertTrue(any("Unclosed @Start block" in item.message for item in kernel.telemetry_logs))


if __name__ == "__main__":
    unittest.main()
