# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

"""Package an Agent Skill directory as a deterministic ZIP archive."""

from __future__ import annotations

import argparse
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys
import zipfile

IGNORED_DIRECTORIES = {".git", "__pycache__"}
IGNORED_FILES = {".DS_Store", ".git"}
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
WINDOWS_INVALID_CHARACTERS = '<>"|?*'
WINDOWS_RESERVED_NAMES = {
    "AUX",
    "CON",
    "NUL",
    "PRN",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
    *(f"COM{number}" for number in "¹²³"),
    *(f"LPT{number}" for number in "¹²³"),
}


def _is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def _is_link_like(path: Path) -> bool:
    is_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or (
        is_junction is not None and is_junction()
    )


def _validate_archive_component(component: str) -> None:
    windows_normalized = component.rstrip(" .")
    if (
        component in {"", ".", ".."}
        or windows_normalized in {"", ".", ".."}
        or component != windows_normalized
        or "/" in component
        or "\\" in component
        or ":" in component
        or any(character in component for character in WINDOWS_INVALID_CHARACTERS)
        or any(ord(character) < 32 for character in component)
        or component.split(".", 1)[0].upper() in WINDOWS_RESERVED_NAMES
    ):
        raise ValueError(f"unsafe archive path component: {component!r}")


def _archive_path(source_name: str, relative: Path) -> str:
    components = (source_name, *relative.parts)
    for component in components:
        _validate_archive_component(component)

    posix_path = PurePosixPath(*components)
    windows_path = PureWindowsPath(*components)
    if (
        posix_path.is_absolute()
        or windows_path.is_absolute()
        or windows_path.drive
        or posix_path.parts != components
        or windows_path.parts != components
        or posix_path.parts[0] != source_name
        or windows_path.parts[0] != source_name
    ):
        raise ValueError(f"archive member escapes skill root: {relative}")

    return posix_path.as_posix()


def _require_skill_file(source: Path) -> None:
    skill_file = next(
        (entry for entry in source.iterdir() if entry.name == "SKILL.md"),
        None,
    )
    if (
        skill_file is None
        or not skill_file.is_file()
        or _is_link_like(skill_file)
    ):
        raise ValueError("source must contain a regular file named exactly SKILL.md")


def _collect_files(source: Path) -> list[tuple[Path, str]]:
    files: list[tuple[Path, str]] = []

    for current, directories, filenames in os.walk(source, followlinks=False):
        current_path = Path(current)
        retained_directories = []
        for name in sorted(directories):
            path = current_path / name
            if name in IGNORED_DIRECTORIES or _is_link_like(path):
                continue
            _validate_archive_component(name)
            retained_directories.append(name)
        directories[:] = retained_directories

        for name in sorted(filenames):
            path = current_path / name
            if (
                name in IGNORED_FILES
                or path.suffix == ".pyc"
                or _is_link_like(path)
            ):
                continue
            relative = path.relative_to(source)
            archive_path = _archive_path(source.name, relative)
            files.append((path, archive_path))

    return sorted(files, key=lambda item: item[1])


def package_skill(source: Path, output: Path, *, overwrite: bool = False) -> Path:
    source = source.expanduser()
    if not source.exists() or not source.is_dir() or _is_link_like(source):
        raise ValueError("source must be an existing non-link directory")

    source = source.resolve()
    _validate_archive_component(source.name)
    _require_skill_file(source)

    output = output.expanduser()
    if output.suffix.lower() != ".zip":
        raise ValueError("output must use the .zip extension")

    resolved_output = output.resolve(strict=False)
    if _is_within(resolved_output, source):
        raise ValueError("output must not be inside the source directory")

    if output.exists() or output.is_symlink():
        if not overwrite:
            raise FileExistsError(f"output already exists: {output}")
        if output.is_dir() and not output.is_symlink():
            raise IsADirectoryError(f"output is a directory: {output}")
        output.unlink()

    files = _collect_files(source)
    output.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(
        output,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path, archive_path in files:
            info = zipfile.ZipInfo(archive_path, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compresslevel=9)

    return output


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package an Agent Skill directory as a deterministic ZIP archive."
    )
    parser.add_argument("source", type=Path, help="skill directory to package")
    parser.add_argument(
        "--output",
        type=Path,
        help="output ZIP path (default: ./<skill-directory>.zip)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing output file",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    output = args.output or Path.cwd() / f"{args.source.resolve().name}.zip"

    try:
        packaged = package_skill(args.source, output, overwrite=args.force)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(packaged)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
