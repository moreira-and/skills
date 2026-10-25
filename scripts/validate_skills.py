#!/usr/bin/env python3
"""Validate the repository's Agent Skills catalog without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ROOT_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
METADATA_KEY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
LOCAL_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
INVALID_PLAIN_START = ("[", "{", "&", "*", "!", "|", ">", "@", "`", "?", ":")


def _scalar(value: str, line: int, errors: list[str]) -> str | None:
    """Parse the simple string-scalar subset used by the catalog contract."""
    value = re.sub(r"\s+#.*$", "", value).strip()
    if not value:
        errors.append(f"line {line}: expected a non-empty string scalar")
        return None
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            parsed = None
        if not isinstance(parsed, str) or not parsed:
            errors.append(f"line {line}: invalid or empty double-quoted string")
            return None
        return parsed
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            errors.append(f"line {line}: invalid single-quoted string")
            return None
        parsed = value[1:-1].replace("''", "'")
        if "'" in parsed or not parsed:
            errors.append(f"line {line}: invalid or empty single-quoted string")
            return None
        return parsed
    if (
        value.startswith(INVALID_PLAIN_START)
        or re.match(r"^(?:~|null|true|false|yes|no|on|off)$", value, re.IGNORECASE)
        or re.fullmatch(r"[-+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)", value)
        or re.search(r":\s", value)
    ):
        errors.append(f"line {line}: quote YAML-reserved or non-string values")
        return None
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object] | None, str, list[str]]:
    """Parse and validate the catalog's deliberately small YAML frontmatter subset."""
    lines = text.splitlines()
    errors: list[str] = []
    if not lines or lines[0].strip() != "---":
        return None, "", ["missing YAML frontmatter opening delimiter"]

    end = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if end is None:
        return None, "", ["missing YAML frontmatter closing delimiter"]

    data: dict[str, object] = {}
    metadata: dict[str, str] = {}
    metadata_open = False
    for number, raw in enumerate(lines[1:end], 2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw:
            errors.append(f"line {number}: tabs are not allowed in YAML frontmatter")
            continue
        if raw.startswith("  "):
            match = re.fullmatch(r"  ([A-Za-z0-9][A-Za-z0-9_.-]*):(?:[ \t]*(.*))?", raw)
            if not metadata_open or not match:
                errors.append(f"line {number}: invalid or unexpected indented frontmatter")
                continue
            key, raw_value = match.groups()
            if key in metadata:
                errors.append(f"line {number}: duplicate metadata key {key!r}")
            else:
                parsed = _scalar(raw_value or "", number, errors)
                if parsed is not None:
                    metadata[key] = parsed
            continue
        match = re.fullmatch(r"([a-z][a-z-]*):(?:[ \t]*(.*))?", raw)
        if not match:
            errors.append(f"line {number}: expected a top-level key and scalar value")
            metadata_open = False
            continue
        key, raw_value = match.groups()
        if key not in ROOT_FIELDS:
            errors.append(f"line {number}: unsupported top-level field {key!r}")
            metadata_open = False
            continue
        if key in data:
            errors.append(f"line {number}: duplicate field {key!r}")
            metadata_open = key == "metadata"
            continue
        if key == "metadata":
            if raw_value and raw_value.strip():
                errors.append(f"line {number}: metadata must be a mapping")
                metadata_open = False
            else:
                data[key] = metadata
                metadata_open = True
            continue
        metadata_open = False
        parsed = _scalar(raw_value or "", number, errors)
        if parsed is not None:
            data[key] = parsed

    body = "\n".join(lines[end + 1 :]).strip()
    if not body:
        errors.append("SKILL.md must contain Markdown instructions after the frontmatter")
    for required in ("name", "description"):
        if required not in data:
            errors.append(f"missing required field {required!r}")
    if "name" in data and not isinstance(data["name"], str):
        errors.append("'name' must be a string")
    if "description" in data and not isinstance(data["description"], str):
        errors.append("'description' must be a string")
    if "metadata" in data:
        data["metadata"] = metadata
    return data, body, errors


def _validate_links(skill_dir: Path, body: str, errors: list[str]) -> None:
    for match in LOCAL_LINK.finditer(body):
        target = match.group(1).strip()
        if target.startswith("<") and ">" in target:
            target = target[1 : target.index(">")]
        else:
            target = target.split(maxsplit=1)[0] if target else ""
        parsed = urlsplit(target)
        if not parsed.path or parsed.scheme or parsed.netloc:
            continue
        path = unquote(parsed.path)
        if len(Path(path).parts) > 2:
            errors.append(f"local link {target!r} is more than one directory deep")
            continue
        resolved = (skill_dir / path).resolve()
        if resolved != skill_dir.resolve() and skill_dir.resolve() not in resolved.parents:
            errors.append(f"local link {target!r} escapes the skill directory")
        elif not resolved.exists():
            errors.append(f"local link {target!r} does not exist")


def _validate_scripts(skill_dir: Path, errors: list[str]) -> None:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.is_dir():
        return
    scripts = sorted(
        path for path in scripts_dir.rglob("*") if path.is_file() and path.name != "README.md"
    )
    if not scripts:
        return
    readme = scripts_dir / "README.md"
    if not readme.is_file():
        errors.append("scripts/README.md is required when scripts are present")
        return
    text = readme.read_text(encoding="utf-8")
    sections = list(re.finditer(r"(?m)^###\s+(.+?)\s*$", text))
    for script in scripts:
        relative = script.relative_to(skill_dir).as_posix()
        section = next((item for item in sections if item.group(1) == relative), None)
        if section is None:
            errors.append(f"scripts/README.md needs a '### {relative}' section")
            continue
        end = next((item.start() for item in sections if item.start() > section.start()), len(text))
        content = text[section.end() : end].casefold()
        if not re.search(r"(?m)^usage\s*:", content):
            errors.append(f"scripts/README.md section for {relative} needs a Usage: entry")
        if not re.search(r"(?m)^dependencies\s*:", content):
            errors.append(f"scripts/README.md section for {relative} needs a Dependencies: entry")


def validate_skill(skill_dir: Path, names: set[str]) -> list[str]:
    errors: list[str] = []
    if skill_dir.is_symlink():
        return ["skill directories must not be symbolic links"]
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file() or skill_file.is_symlink():
        return ["missing regular SKILL.md file"]
    try:
        text = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return [f"cannot read SKILL.md as UTF-8: {error}"]
    data, body, errors = parse_frontmatter(text)
    if data is None:
        return errors

    name = data.get("name")
    if isinstance(name, str):
        if len(name) > 64 or not SKILL_NAME.fullmatch(name):
            errors.append("'name' must be 1–64 lowercase letters, digits, or single hyphens")
        if name != skill_dir.name:
            errors.append(f"name {name!r} must match directory {skill_dir.name!r}")
        if name in names:
            errors.append(f"duplicate skill name {name!r}")
        names.add(name)

    description = data.get("description")
    if isinstance(description, str):
        if len(description) > 1024:
            errors.append("'description' exceeds the 1024-character specification limit")
        if len(description.strip()) < 30:
            errors.append("'description' must contain at least 30 characters")
        if not re.search(r"\buse when\b", description, re.IGNORECASE):
            errors.append("'description' must include the explicit phrase 'Use when'")

    compatibility = data.get("compatibility")
    if isinstance(compatibility, str) and len(compatibility) > 500:
        errors.append("'compatibility' exceeds the 500-character specification limit")
    _validate_links(skill_dir, body, errors)
    _validate_scripts(skill_dir, errors)
    return errors


def validate_catalog(skills_dir: Path) -> list[str]:
    if not skills_dir.exists():
        return []
    if not skills_dir.is_dir():
        return [f"{skills_dir}: skills path is not a directory"]
    errors: list[str] = []
    names: set[str] = set()
    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        for message in validate_skill(skill_dir, names):
            errors.append(f"{skill_dir.name}: {message}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "skills",
        help="directory containing one directory per skill (default: repository skills/)",
    )
    args = parser.parse_args()
    errors = validate_catalog(args.skills_dir)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    skill_count = sum(1 for item in args.skills_dir.iterdir() if item.is_dir()) if args.skills_dir.is_dir() else 0
    print(f"Validated {skill_count} skill(s).")
    if skill_count == 0:
        print("No skills found; the catalog is ready for its first reviewed skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
