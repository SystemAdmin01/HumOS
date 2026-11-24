import unittest
from pathlib import Path

from linghos.syntax import find_block_end, normalize_script
from linghos.parser import LINGHOSParser
from linghos.compiler import LINGHOSCompiler


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


    def test_compiler_reports_unclosed_blocks_without_crashing(self):
        compiler = LINGHOSCompiler()
        malformed_scripts = [
            "@Start>(PRS_VM) {\nON> target;",
            "/SET_Lockdown_Mode {\nTake_DOWN(all) > target;",
            "IF(CS_EXPOSED) {\nCall >> Ice_shield;",
        ]
        for source in malformed_scripts:
            with self.subTest(source=source):
                result = compiler.compile(source)
                self.assertTrue(
                    any(item["level"] == "ERROR" for item in result["compiler_meta"]["diagnostics"])
                )


    def test_repository_examples_are_handled_by_compiler(self):
        examples_dir = Path(__file__).resolve().parents[1] / "examples"
        example_files = sorted(
            path for path in examples_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in {".lgh", ".lghos"}
        )
        self.assertTrue(example_files, "No LINGHOS example scripts were found")

        for path in example_files:
            with self.subTest(example=path.name):
                result = LINGHOSCompiler().compile(path.read_text(encoding="utf-8"))
                self.assertIn("compiler_meta", result)
                self.assertIn("diagnostics", result["compiler_meta"])

    def test_interpreter_reports_unclosed_vm_block_without_crashing(self):
        kernel = LINGHOSParser().execute_script("@Start>(PRS_VM) {\nON> target;")
        self.assertTrue(any("Unclosed @Start block" in item.message for item in kernel.telemetry_logs))


if __name__ == "__main__":
    unittest.main()
