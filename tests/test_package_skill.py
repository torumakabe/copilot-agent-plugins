from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile


SCRIPT_PATH = (
    Path(__file__).parents[1]
    / "plugins"
    / "skill-creator"
    / "skills"
    / "skill-creator"
    / "scripts"
    / "package_skill.py"
)
SPEC = importlib.util.spec_from_file_location("package_skill", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
PACKAGE_SKILL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE_SKILL)


class PackageSkillTests(unittest.TestCase):
    def make_skill(self, root: Path, name: str = "sample-skill") -> Path:
        skill = root / name
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: sample-skill\ndescription: Sample skill.\n---\n",
            encoding="utf-8",
        )
        return skill

    def test_packages_sorted_paths_under_skill_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            (skill / "references").mkdir()
            (skill / "references" / "z.txt").write_text("z", encoding="utf-8")
            (skill / "a.txt").write_text("a", encoding="utf-8")
            (skill / ".DS_Store").write_text("junk", encoding="utf-8")
            (skill / ".git").write_text("gitdir: elsewhere", encoding="utf-8")
            (skill / "__pycache__").mkdir()
            (skill / "__pycache__" / "cache.pyc").write_bytes(b"junk")

            first = root / "first.zip"
            second = root / "second.zip"
            PACKAGE_SKILL.package_skill(skill, first)
            PACKAGE_SKILL.package_skill(skill, second)

            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(
                    archive.namelist(),
                    [
                        "sample-skill/SKILL.md",
                        "sample-skill/a.txt",
                        "sample-skill/references/z.txt",
                    ],
                )
                for entry in archive.infolist():
                    self.assertEqual(entry.create_system, 3)
                    self.assertEqual(entry.date_time, PACKAGE_SKILL.ZIP_TIMESTAMP)
                    self.assertEqual(entry.external_attr >> 16, 0o100644)

    def test_requires_source_and_exact_case_skill_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "output.zip"

            with self.assertRaisesRegex(
                ValueError, "existing non-link directory"
            ):
                PACKAGE_SKILL.package_skill(root / "missing", output)

            skill = root / "wrong-case"
            skill.mkdir()
            (skill / "skill.md").write_text("wrong case", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "exactly SKILL.md"):
                PACKAGE_SKILL.package_skill(skill, output)

    def test_refuses_existing_output_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            output = root / "skill.zip"
            output.write_bytes(b"existing")

            with self.assertRaises(FileExistsError):
                PACKAGE_SKILL.package_skill(skill, output)

            PACKAGE_SKILL.package_skill(skill, output, overwrite=True)
            self.assertTrue(zipfile.is_zipfile(output))

    def test_refuses_output_inside_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)

            with self.assertRaisesRegex(ValueError, "inside the source"):
                PACKAGE_SKILL.package_skill(skill, skill / "package.zip")

    def test_excludes_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            target = root / "outside.txt"
            target.write_text("outside", encoding="utf-8")
            link = skill / "outside-link.txt"
            try:
                link.symlink_to(target)
            except OSError as error:
                self.skipTest(f"symlinks are unavailable: {error}")

            output = root / "skill.zip"
            PACKAGE_SKILL.package_skill(skill, output)

            with zipfile.ZipFile(output) as archive:
                self.assertNotIn("sample-skill/outside-link.txt", archive.namelist())

    @unittest.skipIf(
        os.name == "nt",
        "Windows cannot create these POSIX filenames",
    )
    def test_rejects_names_unsafe_for_windows_extraction(self) -> None:
        for unsafe_name in (
            r"back\slash.txt",
            "C:drive.txt",
            "trailing.",
            *('<bad', '>bad', '"bad', '|bad', '?bad', '*bad'),
        ):
            with self.subTest(unsafe_name=unsafe_name):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    skill = self.make_skill(root)
                    (skill / unsafe_name).write_text("unsafe", encoding="utf-8")

                    with self.assertRaisesRegex(
                        ValueError, "unsafe archive path component"
                    ):
                        PACKAGE_SKILL.package_skill(skill, root / "skill.zip")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            unsafe_source = self.make_skill(root, "C:sample-skill")
            with self.assertRaisesRegex(
                ValueError, "unsafe archive path component"
            ):
                PACKAGE_SKILL.package_skill(
                    unsafe_source,
                    root / "skill.zip",
                )

    def test_rejects_cross_platform_unsafe_components(self) -> None:
        for component in (
            ".",
            "..",
            "...",
            ".. ",
            r"back\slash.txt",
            "C:drive.txt",
            "NUL.txt",
            "com¹.txt",
            "Com²",
            "COM³.log",
            "com¹. ",
            "lpt¹.txt",
            "Lpt²",
            "LPT³.log",
            "lpt³.",
            *('<bad', '>bad', '"bad', '|bad', '?bad', '*bad'),
        ):
            with self.subTest(component=component):
                with self.assertRaisesRegex(
                    ValueError, "unsafe archive path component"
                ):
                    PACKAGE_SKILL._validate_archive_component(component)

    @unittest.skipUnless(
        os.name == "nt" and hasattr(Path, "is_junction"),
        "Windows junctions are unavailable",
    )
    def test_rejects_source_junction_and_prunes_child_junction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target_skill = self.make_skill(root, "target-skill")
            source_junction = root / "source-junction"
            result = subprocess.run(
                [
                    "cmd.exe",
                    "/d",
                    "/c",
                    "mklink",
                    "/J",
                    str(source_junction),
                    str(target_skill),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                self.skipTest(f"cannot create junction: {result.stderr}")

            with self.assertRaisesRegex(ValueError, "non-link directory"):
                PACKAGE_SKILL.package_skill(
                    source_junction,
                    root / "source-junction.zip",
                )

            skill = self.make_skill(root, "real-skill")
            external = root / "external"
            external.mkdir()
            (external / "outside.txt").write_text("outside", encoding="utf-8")
            child_junction = skill / "linked"
            result = subprocess.run(
                [
                    "cmd.exe",
                    "/d",
                    "/c",
                    "mklink",
                    "/J",
                    str(child_junction),
                    str(external),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                self.skipTest(f"cannot create junction: {result.stderr}")

            output = root / "real-skill.zip"
            PACKAGE_SKILL.package_skill(skill, output)
            with zipfile.ZipFile(output) as archive:
                self.assertNotIn(
                    "real-skill/linked/outside.txt",
                    archive.namelist(),
                )


if __name__ == "__main__":
    unittest.main()
