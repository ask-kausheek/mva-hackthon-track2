import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from mva_track2.package import FILES, archive


class PackageTests(unittest.TestCase):
    def test_allowlist_hashes_and_repeatable_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "project"
            root.mkdir()
            for name in FILES:
                path = root.joinpath(*name.split("/"))
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("synthetic file\n", encoding="utf-8")
            (root / "private.vcf").write_text("must not be archived", encoding="utf-8")
            first = Path(temp) / "first.zip"
            second = Path(temp) / "second.zip"
            with patch("mva_track2.package.ROOT", root):
                self.assertEqual(archive(first), len(FILES) + 1)
                archive(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as handle:
                self.assertNotIn("track2/private.vcf", handle.namelist())
                manifest = json.loads(handle.read("track2/ARTIFACT_MANIFEST.json"))
                for name, digest in manifest["files_sha256"].items():
                    self.assertEqual(hashlib.sha256(handle.read(name)).hexdigest(), digest)

    def test_missing_required_file_prevents_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "out.zip"
            with patch("mva_track2.package.ROOT", Path(temp) / "missing"):
                with self.assertRaises(OSError):
                    archive(output)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
