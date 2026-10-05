"""Check channel isolation, retries, failed publication and Prism packaging."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib
import unittest
from unittest.mock import patch
import zipfile

import dev_release
import test_release
from test_release import SCRIPTS


class DevReleaseTests(unittest.TestCase):
    setUp = test_release.ReleaseTests.setUp
    git = test_release.ReleaseTests.git
    pack = test_release.ReleaseTests.pack
    commit = test_release.ReleaseTests.commit

    def env(self, **overrides):
        return {**os.environ, "GITHUB_REF": "refs/heads/dev", "GITHUB_RUN_ID": "42",
                "GITHUB_SHA": self.git("rev-parse", "HEAD"),
                "GITHUB_REPOSITORY": "adraug/rocher-suchard",
                "GITHUB_OUTPUT": str(self.root / ".git/output"), **overrides}

    def prepare_dev(self, env=None):
        output = self.root / ".git/output"
        output.write_text("")
        result = subprocess.run([sys.executable, str(SCRIPTS / "dev_release.py"), "prepare"],
                                cwd=self.root, env=env or self.env(), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return dict(line.split("=", 1) for line in output.read_text().splitlines())

    def test_version_retry_and_stable_allocator(self):
        source = self.git("rev-parse", "HEAD")
        self.git("tag", "v1.1.5")
        self.assertEqual(self.prepare_dev(), {"tag": "dev-42", "reused": "false"})
        self.assertEqual(tomllib.loads((self.root / "pack.toml").read_text())["version"],
                         f"1.1.0-dev.42.g{source[:7]}")
        self.commit("chore: build dev-42")
        self.git("tag", "dev-42")
        self.git("checkout", "-q", "--detach", source)
        self.assertEqual(self.prepare_dev(), {"tag": "dev-42", "reused": "true"})
        self.git("checkout", "-q", "--detach", source)
        self.assertEqual(test_release.ReleaseTests.prepare(self)["tag"], "v1.1.6")

    def test_reject_wrong_branch_checkout_and_tag(self):
        for overrides in ({"GITHUB_REF": "refs/heads/main"}, {"GITHUB_RUN_ID": "bad"},
                          {"GITHUB_SHA": "0" * 40}):
            result = subprocess.run([sys.executable, str(SCRIPTS / "dev_release.py"), "prepare"],
                                    cwd=self.root, env=self.env(**overrides), capture_output=True)
            self.assertNotEqual(result.returncode, 0)
        self.git("tag", "dev-42")
        with self.assertRaises(AssertionError):
            self.prepare_dev()

    def test_prism_bundle_and_checksum(self):
        self.pack("1.2.0-dev.42.gabcdef0")
        with (self.root / "pack.toml").open("a") as out:
            out.write('[versions]\nminecraft="1.21.1"\nneoforge="21.1.251"\n')
        dist = self.root / "dist"
        dist.mkdir()
        (dist / "SHA256SUMS.txt").write_text("a" * 64 + "  other.zip\n")
        bootstrap = self.root / "bootstrap.jar"
        bootstrap.write_bytes(b"fixture bootstrap")
        # prism uses paths relative to the build checkout.
        old = Path.cwd()
        try:
            os.chdir(self.root)
            with patch.dict(os.environ, {"GITHUB_REPOSITORY": "adraug/rocher-suchard"}):
                with self.assertRaisesRegex(ValueError, "checksum"):
                    dev_release.prism(bootstrap)
                with patch.object(dev_release, "BOOTSTRAP_SHA256", hashlib.sha256(bootstrap.read_bytes()).hexdigest()):
                    dev_release.prism(bootstrap)
                    archive = dist / "Rocher-Suchard-DEV-Prism.zip"
                    before = archive.read_bytes()
                    dev_release.prism(bootstrap)
                    self.assertEqual(before, archive.read_bytes())
                    with zipfile.ZipFile(archive) as z:
                        self.assertEqual(len(z.namelist()), 4)
                        self.assertEqual(z.read('.minecraft/packwiz-installer-bootstrap.jar'), bootstrap.read_bytes())
                        cfg = z.read("instance.cfg").decode()
                        command = json.loads(next(x.split("=", 1)[1] for x in cfg.splitlines() if x.startswith("PreLaunchCommand=")))
                        self.assertIn('"$INST_JAVA"', command)
                        self.assertIn('"$INST_MC_DIR/packwiz-installer-bootstrap.jar"', command)
                        self.assertIn('/refs/heads/dev-latest/pack.toml', command)
                        self.assertIn('-s client', command)
                        components = json.loads(z.read('mmc-pack.json'))['components']
                        self.assertEqual(components[1], {'uid':'net.neoforged','version':'21.1.251','important':True})
                    lines = (dist / "SHA256SUMS.txt").read_text().splitlines()
                    self.assertEqual(len(lines), 2)
                    self.assertIn(hashlib.sha256(before).hexdigest() + "  " + archive.name, lines)
        finally:
            os.chdir(old)

    def publication_fixture(self):
        source = self.git("rev-parse", "HEAD")
        self.git("branch", "-M", "dev")
        remote = self.root / ".git/remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
        self.git("remote", "add", "origin", str(remote))
        self.git("branch", "latest")
        self.git("tag", "v1.1.0")
        self.git("push", "-q", "origin", "dev", "latest", "v1.1.0")
        self.prepare_dev()
        (self.root / "index.toml").write_text('hash-format="sha256"\n')
        dist = self.root / "dist"
        dist.mkdir()
        (dist / "SHA256SUMS.txt").write_text("0" * 64 + "  pack.toml\n")
        (dist / "pack.toml").write_text("fixture")
        binary = self.root / ".git/bin"
        binary.mkdir()
        fake = binary / "gh"
        fake.write_text(f'#!{sys.executable}\n' + '''import json, os, pathlib, sys
args=sys.argv[1:]
root=pathlib.Path(os.environ['FAKE_GH_ROOT'])
with (root/'calls').open('a') as f: f.write(json.dumps(args)+'\\n')
state=root/'state'
if args[0]=='api':
    print('dev-42' if state.exists() else '')
elif args[:2]==['release','create']:
    assert '--prerelease' in args and '--latest=false' in args and args[2]=='dev-42'
    state.write_text('draft')
elif args[:2]==['release','view']:
    print(str(state.read_text()=='draft').lower() if 'isDraft' in args else 'true')
elif args[:2]==['release','upload']:
    if os.environ.get('FAIL_UPLOAD'): sys.exit(1)
elif args[:2]==['release','edit']:
    assert '--prerelease' in args and '--latest=false' in args
    state.write_text('published')
else: raise RuntimeError(args)
''')
        fake.chmod(0o755)
        return self.env(GITHUB_SHA=source, TAG="dev-42", REUSED="false", GH_REPO="adraug/rocher-suchard",
                        RUNNER_TEMP=str(self.root / ".git"), FAKE_GH_ROOT=str(self.root / ".git"),
                        PATH=str(binary) + os.pathsep + os.environ["PATH"])

    def publish(self, env):
        return subprocess.run(["bash", str(SCRIPTS / "publish_dev.sh")], cwd=self.root,
                              env=env, text=True, capture_output=True)

    def test_publish_and_retry_preserve_stable(self):
        env = self.publication_fixture()
        result = self.publish(env)
        self.assertEqual(result.returncode, 0, result.stderr)
        published = self.git("rev-parse", "dev-42")
        self.assertTrue(self.git("ls-remote", "origin", "refs/heads/dev-latest").startswith(published))
        self.assertTrue(self.git("ls-remote", "origin", "refs/heads/latest").startswith(env['GITHUB_SHA']))
        self.assertEqual(self.git("rev-parse", "v1.1.0"), env['GITHUB_SHA'])
        self.assertEqual(self.publish({**env, "REUSED":"true"}).returncode, 0)
        calls = [json.loads(x) for x in (self.root / '.git/calls').read_text().splitlines()]
        self.assertEqual(sum(x[:2]==['release','upload'] for x in calls), 1)

    def test_failed_upload_then_retry(self):
        env = self.publication_fixture()
        self.assertNotEqual(self.publish({**env, "FAIL_UPLOAD":"1"}).returncode, 0)
        self.assertEqual(self.git("ls-remote", "origin", "refs/heads/dev-latest"), "")
        result = self.publish({**env, "REUSED":"true"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotEqual(self.git("ls-remote", "origin", "refs/heads/dev-latest"), "")

    def test_old_build_cannot_promote(self):
        env = self.publication_fixture()
        # Move only the remote source branch, simulating a newer push during build.
        newer = self.git("commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", "newer dev")
        self.git("push", "-q", "origin", f"{newer}:refs/heads/dev")
        result = self.publish(env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git("ls-remote", "origin", "refs/heads/dev-latest"), "")
        self.assertTrue(self.git("ls-remote", "origin", "refs/heads/latest").startswith(env['GITHUB_SHA']))


if __name__ == '__main__':
    unittest.main()
