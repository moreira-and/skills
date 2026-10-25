"""Heuristic checks for SQL and Python Lakeflow pipeline definition files.

This regular-expression-based checker is not a SQL parser and does not replace
bundle validation or execution in a Databricks workspace. It reports common
imperative patterns and incomplete declarative constructs before deployment.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass
class Finding:
    file: str
    line: int
    severity: Severity
    rule: str
    message: str
    snippet: str

    def format(self) -> str:
        return (
            f"[{self.severity.value}] {self.file}:{self.line} ({self.rule})\n"
            f"    {self.message}\n"
            f"    > {self.snippet.strip()}"
        )


def _line_of(text: str, keyword: str) -> int:
    position = text.upper().find(keyword.upper())
    if position == -1:
        return 1
    return text[:position].count("\n") + 1


def _snippet_of(text: str, keyword: str, width: int = 80) -> str:
    position = text.upper().find(keyword.upper())
    if position == -1:
        return keyword
    start = max(0, position - width // 2)
    end = min(len(text), position + width // 2)
    return text[start:end].replace("\n", " ")


_SQL_SCRIPTING_PATTERN = re.compile(r"^\s*(BEGIN|DECLARE|SET\s+\w)", re.IGNORECASE)
_MERGE_PATTERN = re.compile(r"^\s*MERGE\s+INTO\b", re.IGNORECASE)
_INSERT_REPLACE_PATTERN = re.compile(
    r"\bINSERT\s+INTO\b.*?\bREPLACE\s+WHERE\b", re.IGNORECASE | re.DOTALL
)
_CREATE_TABLE_PLAIN_PATTERN = re.compile(
    r"CREATE\s+(?:OR\s+REPLACE\s+)?TABLE\b", re.IGNORECASE
)
_CREATE_STREAMING_TABLE_PATTERN = re.compile(
    r"CREATE\s+(?:OR\s+REFRESH\s+)?STREAMING\s+TABLE\s+([\w.`]+)", re.IGNORECASE
)
_CREATE_MATERIALIZED_VIEW_PATTERN = re.compile(
    r"CREATE\s+(?:OR\s+REFRESH\s+)?MATERIALIZED\s+VIEW\s+([\w.`]+)",
    re.IGNORECASE,
)
_APPLY_CHANGES_PATTERN = re.compile(
    r"APPLY\s+CHANGES\s+INTO\s+([\w.`]+)(.*?);", re.IGNORECASE | re.DOTALL
)
_KEYS_PATTERN = re.compile(r"\bKEYS\s*\(", re.IGNORECASE)
_SEQUENCE_BY_PATTERN = re.compile(r"\bSEQUENCE\s+BY\b", re.IGNORECASE)
_STORED_AS_SCD_PATTERN = re.compile(r"\bSTORED\s+AS\s+SCD\s+TYPE\s+[12]\b", re.IGNORECASE)
_STREAM_SOURCE_PATTERN = re.compile(r"\bSTREAM\s*\(", re.IGNORECASE)
_CLUSTER_BY_PATTERN = re.compile(r"\bCLUSTER\s+BY\b", re.IGNORECASE)
_CONSTRAINT_EXPECT_PATTERN = re.compile(
    r"CONSTRAINT\s+\w+\s+EXPECT\s*\([^)]*\)(\s+ON\s+VIOLATION\s+[\w\s]+?)?(?=,|\)|\n|$)",
    re.IGNORECASE,
)
_ON_VIOLATION_VALUE_PATTERN = re.compile(
    r"ON\s+VIOLATION\s+(DROP\s+ROW|FAIL\s+UPDATE)\b", re.IGNORECASE
)


def check_sql(text: str, filename: str) -> list[Finding]:
    findings: list[Finding] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        if _SQL_SCRIPTING_PATTERN.match(line):
            findings.append(
                Finding(
                    filename,
                    line_number,
                    Severity.ERROR,
                    "sql-scripting-nao-suportado",
                    "BEGIN/DECLARE/SET de SQL Scripting não são suportados dentro de "
                    "arquivos de definição de Lakeflow Declarative Pipelines. Use "
                    "CREATE STREAMING TABLE / CREATE MATERIALIZED VIEW / APPLY CHANGES INTO.",
                    line,
                )
            )
        if _MERGE_PATTERN.match(line):
            findings.append(
                Finding(
                    filename,
                    line_number,
                    Severity.ERROR,
                    "merge-manual",
                    "MERGE INTO manual não é o padrão declarativo. Para upsert/CDC/dedupe "
                    "por chave, avalie APPLY CHANGES INTO e confirme equivalência semântica.",
                    line,
                )
            )

    if _INSERT_REPLACE_PATTERN.search(text):
        findings.append(
            Finding(
                filename,
                _line_of(text, "REPLACE WHERE"),
                Severity.ERROR,
                "insert-replace-where",
                "INSERT INTO ... REPLACE WHERE é padrão imperativo. Modele a transformação "
                "declarativamente sem perder a intenção de reprocessamento/substituição.",
                _snippet_of(text, "REPLACE WHERE"),
            )
        )

    streaming_tables = _CREATE_STREAMING_TABLE_PATTERN.findall(text)
    materialized_views = _CREATE_MATERIALIZED_VIEW_PATTERN.findall(text)
    plain_tables = _CREATE_TABLE_PLAIN_PATTERN.findall(text)

    if plain_tables and not streaming_tables and not materialized_views:
        findings.append(
            Finding(
                filename,
                1,
                Severity.WARNING,
                "create-table-plain",
                "CREATE TABLE simples encontrado. Confirme se é intencional ou se o objeto "
                "deveria ser streaming table ou materialized view.",
                "CREATE TABLE ...",
            )
        )

    for match in _APPLY_CHANGES_PATTERN.finditer(text):
        target, body = match.group(1), match.group(2)
        line_number = text[: match.start()].count("\n") + 1
        clause_preview = match.group(0)[:160]

        if not _KEYS_PATTERN.search(body):
            findings.append(
                Finding(
                    filename,
                    line_number,
                    Severity.ERROR,
                    "apply-changes-sem-keys",
                    f"APPLY CHANGES INTO {target} sem cláusula KEYS (...).",
                    clause_preview,
                )
            )

        if not _SEQUENCE_BY_PATTERN.search(body):
            findings.append(
                Finding(
                    filename,
                    line_number,
                    Severity.ERROR,
                    "apply-changes-sem-sequence-by",
                    f"APPLY CHANGES INTO {target} sem cláusula SEQUENCE BY.",
                    clause_preview,
                )
            )

        if not _STORED_AS_SCD_PATTERN.search(body):
            findings.append(
                Finding(
                    filename,
                    line_number,
                    Severity.WARNING,
                    "apply-changes-scd-implicito",
                    f"APPLY CHANGES INTO {target} sem tipo SCD explícito. Declare a estratégia "
                    "apropriada e confirme a sintaxe na versão-alvo.",
                    clause_preview,
                )
            )

    if streaming_tables and "SELECT" in text.upper() and not _STREAM_SOURCE_PATTERN.search(text):
        findings.append(
            Finding(
                filename,
                1,
                Severity.WARNING,
                "streaming-table-sem-stream",
                "Streaming table com SELECT sem STREAM(...). Confirme a incrementalidade "
                "da fonte e a forma de leitura exigida pela versão-alvo.",
                "SELECT ... FROM <origem sem STREAM(...)>",
            )
        )

    if (streaming_tables or materialized_views) and not _CLUSTER_BY_PATTERN.search(text):
        findings.append(
            Finding(
                filename,
                1,
                Severity.WARNING,
                "sem-cluster-by",
                "Nenhum CLUSTER BY encontrado. Avalie se clustering é apropriado para o objeto "
                "e versão; a ausência não é erro universal.",
                "CREATE STREAMING TABLE / CREATE MATERIALIZED VIEW ...",
            )
        )

    for match in _CONSTRAINT_EXPECT_PATTERN.finditer(text):
        full_clause = match.group(0)
        line_number = text[: match.start()].count("\n") + 1
        has_on_violation = "ON VIOLATION" in full_clause.upper()

        if not has_on_violation:
            findings.append(
                Finding(
                    filename,
                    line_number,
                    Severity.WARNING,
                    "expect-sem-on-violation",
                    "CONSTRAINT ... EXPECT sem ON VIOLATION explícito. Confirme se manter a "
                    "linha é a intenção para esta regra.",
                    full_clause[:120],
                )
            )
        elif not _ON_VIOLATION_VALUE_PATTERN.search(full_clause):
            findings.append(
                Finding(
                    filename,
                    line_number,
                    Severity.ERROR,
                    "expect-on-violation-invalido",
                    "Valor de ON VIOLATION diferente dos valores reconhecidos por este "
                    "validador heurístico; confirme a gramática da versão-alvo.",
                    full_clause[:120],
                )
            )

    for object_name in streaming_tables + materialized_views:
        clean_name = object_name.strip("`")
        if clean_name.count(".") < 2:
            findings.append(
                Finding(
                    filename,
                    1,
                    Severity.WARNING,
                    "nome-nao-qualificado",
                    f"Objeto '{clean_name}' não parece totalmente qualificado "
                    "(catalog.schema.table). Confirme as convenções do projeto.",
                    clean_name,
                )
            )

    return findings


_IMPORT_DLT_PATTERN = re.compile(r"^\s*import\s+dlt\b", re.IGNORECASE | re.MULTILINE)
_DECORATOR_TABLE_PATTERN = re.compile(
    r"@(?:dlt|dp)\.(?:table|materialized_view|view|append_flow)\b"
)
_SPARK_WRITE_PATTERN = re.compile(
    r"\bspark\.sql\s*\(\s*[\"'].*?\b(INSERT|MERGE|DELETE|UPDATE)\b",
    re.IGNORECASE | re.DOTALL,
)


def check_python(text: str, filename: str) -> list[Finding]:
    findings: list[Finding] = []

    if _IMPORT_DLT_PATTERN.search(text):
        findings.append(
            Finding(
                filename,
                _line_of(text, "import dlt"),
                Severity.WARNING,
                "import-dlt-legado",
                "Uso de 'import dlt'. Confirme o import correto na documentação vigente da "
                "versão do Databricks Runtime antes de assumir compatibilidade.",
                "import dlt",
            )
        )

    if not _DECORATOR_TABLE_PATTERN.search(text):
        findings.append(
            Finding(
                filename,
                1,
                Severity.WARNING,
                "sem-decorator-pipeline",
                "Nenhum decorator de pipeline reconhecido. Confirme se o arquivo define "
                "objetos de pipeline e se a API usada pertence à versão-alvo.",
                "@dlt.table / @dp.table ...",
            )
        )

    for match in _SPARK_WRITE_PATTERN.finditer(text):
        findings.append(
            Finding(
                filename,
                text[: match.start()].count("\n") + 1,
                Severity.ERROR,
                "spark-sql-imperativo",
                "spark.sql(...) executa escrita imperativa dentro de uma definição de "
                "pipeline. Confirme o contrato declarativo antes de publicar.",
                match.group(0)[:120],
            )
        )

    return findings


def run_file(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix == ".sql":
        return check_sql(text, str(path))
    if suffix == ".py":
        return check_python(text, str(path))
    raise ValueError(f"Extensão não suportada: {path.suffix or '(sem extensão)'}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validador heurístico para definições SQL/Python de pipelines Lakeflow."
    )
    parser.add_argument("paths", nargs="*", help="Arquivos .sql/.py a validar.")
    parser.add_argument("--dir", help="Valida recursivamente os .sql/.py de uma pasta.")
    args = parser.parse_args(argv)

    targets = [Path(path) for path in args.paths]
    if args.dir:
        base = Path(args.dir)
        if not base.is_dir():
            parser.error(f"Diretório não encontrado ou inválido: {base}")
        targets.extend(sorted(base.rglob("*.sql")))
        targets.extend(sorted(base.rglob("*.py")))

    if not targets:
        parser.error("Informe arquivos .sql/.py ou um diretório existente com esses arquivos.")

    all_findings: list[Finding] = []
    input_errors = 0
    for path in targets:
        if not path.exists():
            print(f"[ERROR] Arquivo não encontrado: {path}", file=sys.stderr)
            input_errors += 1
            continue
        if not path.is_file():
            print(f"[ERROR] O caminho não é um arquivo regular: {path}", file=sys.stderr)
            input_errors += 1
            continue
        if path.suffix.lower() not in {".sql", ".py"}:
            print(f"[ERROR] Extensão não suportada: {path}", file=sys.stderr)
            input_errors += 1
            continue
        try:
            all_findings.extend(run_file(path))
        except (OSError, UnicodeError, ValueError) as error:
            print(f"[ERROR] Não foi possível validar {path}: {error}", file=sys.stderr)
            input_errors += 1

    for finding in all_findings:
        print(finding.format())
        print()

    errors = sum(finding.severity == Severity.ERROR for finding in all_findings)
    warnings = sum(finding.severity == Severity.WARNING for finding in all_findings)
    if all_findings or input_errors:
        print(
            f"Resumo: {errors + input_errors} erro(s), {warnings} aviso(s).",
            file=sys.stderr if input_errors else sys.stdout,
        )
    else:
        print("Nenhum problema encontrado.")

    return 1 if errors or input_errors else 0


if __name__ == "__main__":
    sys.exit(main())