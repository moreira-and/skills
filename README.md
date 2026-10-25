# Corporate Agent Skills Catalog

This repository is the foundation for reusable corporate skills for LLM agents. Its portable catalog includes four capabilities: Databricks SQL quality, Lakeflow pipeline authoring/operations, PySpark-to-Lakeflow migration, and a migration specialist that orchestrates the other three.

## Structure

```text
skills/
  <skill-name>/
    SKILL.md          # Required metadata and essential instructions
    references/       # Optional, focused supporting material
    scripts/          # Optional, deterministic tools with documented usage
```

## Current Skills

- `databricks-sql-quality/`: organizational SQL naming, typing, documentation, and readability conventions.
- `lakeflow-pipelines/`: Lakeflow object selection, incremental processing, CDC, data quality, and operations.
- `pyspark-to-lakeflow/`: a gated migration process for converting imperative PySpark pipelines to declarative SQL/DABs.
- `databricks-migration-engineer/`: a senior data-engineer persona for Databricks migrations. It defines the workflow, safety limits, and report format, and defers technical rules to the three skills above by name. It never deploys, commits, or pushes, and acts only in a test workspace. In Genie Code, install all four skills side by side under `Workspace/.assistant/skills/`; these limits are instructions, not enforced permissions, and invocation and permissions depend on the consumer.

These portable catalog entries are separate from Copilot command skills under `.github/skills/`; catalog presence alone does not install or expose a skill to every agent consumer.

Create `references/` and `scripts/` only when needed. Keep each skill's detailed guidance in focused reference files and link to them explicitly from `SKILL.md`. Use relative links from the skill root, no more than one directory deep. Put executable tools in `scripts/`; document each tool's usage and dependencies in `scripts/README.md`.

## Skill contract

The catalog follows the [Agent Skills specification](https://agentskills.io/specification). Every `SKILL.md` has YAML frontmatter followed by Markdown instructions:

```yaml
---
name: example-capability
description: Explains the specific task this skill performs and its activation boundary. Use when a request needs this capability.
---
```

`name` and `description` are the only required metadata. Names MUST be 1–64 lowercase ASCII letters, numbers, or single hyphens; they MUST start and end with a letter or number, contain no `--`, be unique, and match the skill directory. Descriptions MUST be 1–1024 characters. This catalog additionally requires at least 30 characters and the explicit phrase `Use when` so reviewers and the validator can check for both capability and activation context. These extra description rules are catalog policy, not Agent Skills requirements.

The specification also permits `license`, `compatibility` (up to 500 characters), `metadata` (string keys and values), and experimental `allowed-tools` (space-separated string). Use an optional field only when applicable; omit `compatibility` if there are no special environment requirements, and avoid `allowed-tools` unless the intended consumer supports it. Do not add custom top-level fields. Keep quoted YAML values simple; descriptions that contain YAML punctuation should be quoted.

The dependency-free validator accepts single-line YAML string scalars (plain, single-quoted, or JSON-compatible double-quoted) and a two-space-indented `metadata` mapping. It intentionally rejects YAML features outside this small catalog contract, such as folded or multiline values, anchors, and tags; use a simple quoted scalar instead.

The body should state the skill's purpose and scope, when not to use it, and short operational steps. Distinguish mandatory rules from recommendations and examples. Link local references and script instructions explicitly. Detailed quality and semantic-review criteria are in the [constitution](.specify/memory/constitution.md).

## Create, validate, and review

1. Add `skills/<unique-name>/SKILL.md` with the contract above. Add focused references and/or scripts only when they contribute real value.

2. When adding scripts, create `scripts/README.md` with a `### scripts/<file>` section for every script and `Usage:` and `Dependencies:` entries. State `None` when a script has no external dependencies.

3. Set up the pinned Python environment and Git hooks with [uv](https://docs.astral.sh/uv/):

   ```bash
   uv sync --locked
   uv run --locked pre-commit install --install-hooks
   uv run --locked python scripts/validate_skills.py
   uv run --locked python -m unittest discover -s tests -v
   ```

   `pyproject.toml` declares the supported Python version and development tools; `uv.lock` pins the resolved environment. The validator and tests use only the Python standard library. Add dependencies with `uv add` or `uv add --dev` and commit the updated lockfile.

4. In VS Code, install the recommended Python extension and run `uv sync --locked` from the repository root. Workspace settings select `.venv` as the interpreter and enable terminal activation. The checked-in interpreter path targets Linux/macOS; on Windows, select `.venv\Scripts\python.exe` with **Python: Select Interpreter**.

   The validator checks metadata and names, description rules, relative local Markdown links, and script documentation. It exits successfully when the catalog has no skills; it does not create a placeholder skill.

5. Git hooks run automatically after installation: `pre-commit` runs Ruff, Markdown formatting checks, and Codespell on applicable changed files; `pre-push` runs the unit tests. Run all lint hooks manually with `uv run --locked pre-commit run --all-files`, and simulate the push hook with `uv run --locked pre-commit run --hook-stage pre-push --all-files`.

6. Review semantic quality separately: one responsibility, correct activation and non-activation boundaries, concise but sufficient instructions, safe behavior, no contradictions or redundancy, valid references, and usefulness of each script. Structural checks cannot judge these properties.

7. For a material change, specify, plan, task, implement, and verify with Spec Kit. Trivial corrections can use direct review with relevant checks.

## Spec Kit

This repository was initialized with the official Specify CLI **1.2.3**, GitHub Copilot integration, and Python scripts. Shared configuration and working templates are in `.specify/`; Copilot command skills are in `.github/skills/`. The setup command was verified here:

```bash
uv tool install specify-cli
specify init --here --force --non-interactive --integration copilot --script py
specify check
```

`specify init --here --force` may replace files at Spec Kit-managed paths. Review and commit existing work before using it; routine contributors do not need to reinitialize the project. `specify check` verifies available integration tooling.

Run the following in the coding agent's chat, **not** in the terminal. For a material change, use `/speckit-constitution` when principles need amendment, then `/speckit-specify`, `/speckit-clarify` when requirements are ambiguous, `/speckit-plan`, `/speckit-checklist` and `/speckit-tasks`, `/speckit-analyze` when useful, `/speckit-implement`, and `/speckit-converge`. The constitution allows lightweight direct review for trivial changes. Agent invocation syntax varies; Copilot uses `/speckit-*`.

## Compatibility limits and importing existing skills

Agent Skills standardizes the skill directory and `SKILL.md` format, not how every agent discovers, invokes, or authorizes skills. Consumer-specific search paths, frontmatter extensions, available tools, and resource-loading behavior differ. This repository's Copilot commands use `.github/skills/`; skills under `skills/` remain a portable catalog and are not automatically installed or exposed to every agent. Test discovery and permissions with each intended consumer, and document any adapter or deviation.

Before importing existing material, inventory it, identify duplicate or overlapping capabilities, and preserve provenance and applicable licenses. Consolidate each capability into one skill with standard metadata, move detailed content into focused references, document scripts, then run structural validation and semantic review. Do not bulk-convert unreviewed content or create skills to represent gaps.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Spec Kit](https://github.com/github/spec-kit) and [existing-project adoption guide](https://github.github.io/spec-kit/guides/existing-projects.html)
