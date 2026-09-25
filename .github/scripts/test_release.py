"""Exercise version allocation and release packaging in disposable repositories."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest
import zipfile


SCRIPTS = Path(__file__).resolve().parent


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Release test")
        self.git("config", "user.email", "test@example.invalid")
        self.pack("1.1")
        self.commit("source")

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def pack(self, version):
        (self.root / "pack.toml").write_text(f'name = "Test Pack"\nversion = "{version}"\n')

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def prepare(self):
        output = self.root / ".git/output"
        output.write_text("")
        subprocess.run([sys.executable, str(SCRIPTS / "release.py")], cwd=self.root,
                       env={**os.environ, "GITHUB_OUTPUT": str(output)}, check=True,
                       stdout=subprocess.DEVNULL)
        return dict(line.split("=", 1) for line in output.read_text().splitlines())

    def test_first_release_and_retry(self):
        source = self.git("rev-parse", "HEAD")
        self.assertEqual(self.prepare(), {"tag": "v1.1.0", "previous_tag": "", "reused": "false"})
        self.commit("chore: release v1.1.0")
        self.git("tag", "v1.1.0")
        self.git("checkout", "-q", "--detach", source)
        self.assertEqual(self.prepare()["reused"], "true")
        self.assertEqual(tomllib.loads((self.root / "pack.toml").read_text())["version"], "1.1.0")

    def test_next_patch_and_new_series(self):
        self.git("tag", "v1.1.0")
        self.assertEqual(self.prepare()["tag"], "v1.1.1")
        self.pack("1.2")
        self.assertEqual(self.prepare()["tag"], "v1.2.0")
        self.pack("1.0")
        self.assertEqual(self.prepare()["tag"], "v1.1.1")

    def test_assets_and_corrupt_index_entry(self):
        config = self.root / "config/example.toml"
        config.parent.mkdir()
        config.write_text("enabled = true\n")
        index = self.root / "index.toml"
        index.write_text('hash-format = "sha256"\n[[files]]\nfile = "config/example.toml"\n'
                         f'hash = "{hashlib.sha256(config.read_bytes()).hexdigest()}"\n')
        with (self.root / "pack.toml").open("a") as pack:
            pack.write('[index]\nfile = "index.toml"\nhash-format = "sha256"\n'
                       f'hash = "{hashlib.sha256(index.read_bytes()).hexdigest()}"\n'
                       '[versions]\nminecraft = "1.21.1"\nneoforge = "21.1.251"\n')
        egg = self.root / "egg/egg-rocher-suchard-packwiz-neoforge.json"
        egg.parent.mkdir()
        egg.write_text("{}\n")
        dist = self.root / "dist"
        dist.mkdir()
        (dist / "stale.mrpack").write_text("must not publish")
        with zipfile.ZipFile(dist / "Test Pack-1.1.mrpack", "w") as archive:
            archive.writestr("modrinth.index.json", json.dumps({"versionId": "1.1", "dependencies":
                             {"minecraft": "1.21.1", "neoforge": "21.1.251"}}))
        def build():
            return subprocess.run([sys.executable, str(SCRIPTS / "release_assets.py")],
                                  cwd=self.root, capture_output=True, text=True)
        result = build()
        self.assertEqual(result.returncode, 0, result.stderr)
        checksums = (dist / "SHA256SUMS.txt").read_text().splitlines()
        self.assertEqual(len(checksums), 5)
        for line in checksums:
            digest, name = line.split("  ", 1)
            self.assertEqual(hashlib.sha256((dist / name).read_bytes()).hexdigest(), digest)
            self.assertNotEqual(name, "stale.mrpack")
        source = dist / "Rocher-Suchard-1.1-packwiz.zip"
        before = source.read_bytes()
        with zipfile.ZipFile(source) as archive:
            self.assertEqual(set(archive.namelist()), {"pack.toml", "index.toml", "config/example.toml"})
            self.assertEqual(archive.read("config/example.toml"), config.read_bytes())
        self.assertEqual(build().returncode, 0)
        self.assertEqual(source.read_bytes(), before)
        config.write_text("changed = true\n")
        result = build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Packwiz hash mismatch", result.stderr)


if __name__ == "__main__":
    unittest.main()
