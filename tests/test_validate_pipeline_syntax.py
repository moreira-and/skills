import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "lakeflow-pipelines"
    / "scripts"
    / "validate_pipeline_syntax.py"
)


class ValidatePipelineSyntaxTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.directory = Path(self.temporary_directory.name)

    def run_script(self, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, arguments)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_accepts_sql_without_findings(self):
        sql_file = self.directory / "simple.sql"
        sql_file.write_text("SELECT 1;\n", encoding="utf-8")

        result = self.run_script(sql_file)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Nenhum problema encontrado", result.stdout)

    def test_accepts_python_pipeline_definition_without_findings(self):
        python_file = self.directory / "pipeline.py"
        python_file.write_text("@dp.table\ndef source():\n    return None\n", encoding="utf-8")

        result = self.run_script(python_file)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Nenhum problema encontrado", result.stdout)

    def test_error_finding_returns_nonzero(self):
        sql_file = self.directory / "imperative.sql"
        sql_file.write_text("MERGE INTO target USING source ON target.id = source.id;\n", encoding="utf-8")

        result = self.run_script(sql_file)

        self.assertEqual(result.returncode, 1)
        self.assertIn("[ERROR]", result.stdout)
        self.assertIn("merge-manual", result.stdout)

    def test_warning_finding_does_not_fail(self):
        python_file = self.directory / "legacy_api.py"
        python_file.write_text("import dlt\n@dlt.table\ndef source():\n    return None\n", encoding="utf-8")

        result = self.run_script(python_file)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[WARNING]", result.stdout)
        self.assertIn("import-dlt-legado", result.stdout)

    def test_missing_file_returns_nonzero(self):
        missing_file = self.directory / "missing.sql"

        result = self.run_script(missing_file)

        self.assertEqual(result.returncode, 1)
        self.assertIn("Arquivo não encontrado", result.stderr)

    def test_directory_passed_as_file_returns_nonzero(self):
        result = self.run_script(self.directory)

        self.assertEqual(result.returncode, 1)
        self.assertIn("não é um arquivo regular", result.stderr)

    def test_invalid_directory_argument_returns_nonzero(self):
        missing_directory = self.directory / "missing"

        result = self.run_script("--dir", missing_directory)

        self.assertEqual(result.returncode, 2)
        self.assertIn("Diretório não encontrado ou inválido", result.stderr)


if __name__ == "__main__":
    unittest.main()