"""Prepare isolated development versions and a self-updating Prism instance."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tomllib
import zipfile

BOOTSTRAP_SHA256 = "a8fbb24dc604278e97f4688e82d3d91a318b98efc08d5dbfcbcbcab6443d116c"


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def prepare():
    if os.environ.get("GITHUB_REF") != "refs/heads/dev":
        raise ValueError("Development releases may only be built from dev")
    run_id = os.environ["GITHUB_RUN_ID"]
    if not re.fullmatch(r"[1-9][0-9]*", run_id):
        raise ValueError("Invalid workflow run ID")
    source = git("rev-parse", "HEAD")
    if source != os.environ["GITHUB_SHA"]:
        raise ValueError("Checkout must match the triggering source commit")
    tag = f"dev-{run_id}"
    reused = tag in git("tag", "--list", tag).splitlines()
    if reused:
        if (git("show", "-s", "--format=%P", tag) != source
                or git("show", "-s", "--format=%s", tag) != f"chore: build {tag}"):
            raise ValueError("Existing development tag belongs to another build")
        git("checkout", "--detach", tag)
    else:
        path = Path("pack.toml")
        content = path.read_text()
        base = tomllib.loads(content)["version"]
        if not re.fullmatch(r"\d+\.\d+(?:\.\d+)?", base):
            raise ValueError("Expected a stable source version in pack.toml")
        if base.count(".") == 1:
            base += ".0"
        version = f"{base}-dev.{run_id}.g{source[:7]}"
        content, count = re.subn(r'^version = "[^"]+"$', f'version = "{version}"',
                                 content, count=1, flags=re.M)
        if count != 1:
            raise ValueError("Missing pack version")
        path.write_text(content)
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        output.write(f"tag={tag}\nreused={str(reused).lower()}\n")


def prism(bootstrap):
    data = Path(bootstrap).read_bytes()
    if hashlib.sha256(data).hexdigest() != BOOTSTRAP_SHA256:
        raise ValueError("Unexpected Packwiz bootstrap checksum")
    pack = tomllib.loads(Path("pack.toml").read_text())
    if "-dev." not in pack["version"]:
        raise ValueError("Prism DEV bundle requires a development version")
    repository = os.environ["GITHUB_REPOSITORY"]
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", repository):
        raise ValueError("Invalid GitHub repository")
    url = f"https://raw.githubusercontent.com/{repository}/refs/heads/dev-latest/pack.toml"
    command = f'"$INST_JAVA" -jar "$INST_MC_DIR/packwiz-installer-bootstrap.jar" --pack-folder "$INST_MC_DIR" -s client {url}'
    # QSettings INI escaping preserves quotes and paths containing spaces.
    cfg = ("[General]\nInstanceType=OneSix\nname=Rocher Suchard DEV\n"
           "OverrideCommands=true\nPreLaunchCommand=" + json.dumps(command) + "\n"
           "OverrideMemory=true\nMinMemAlloc=1024\nMaxMemAlloc=6144\n")
    manifest = {"formatVersion": 1, "components": [
        {"uid": "net.minecraft", "version": pack["versions"]["minecraft"], "important": True},
        {"uid": "net.neoforged", "version": pack["versions"]["neoforge"], "important": True},
    ]}
    target = Path("dist/Rocher-Suchard-DEV-Prism.zip")
    target.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in {
            "instance.cfg": cfg.encode(),
            "LICENSE-packwiz-bootstrap.txt": Path(__file__).with_name("packwiz-bootstrap-LICENSE.txt").read_bytes(),
            "mmc-pack.json": json.dumps(manifest, indent=2).encode(),
            ".minecraft/packwiz-installer-bootstrap.jar": data,
        }.items():
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    checksums = Path("dist/SHA256SUMS.txt")
    lines = [line for line in checksums.read_text().splitlines()
             if not line.endswith("  " + target.name)]
    lines.append(f"{hashlib.sha256(target.read_bytes()).hexdigest()}  {target.name}")
    checksums.write_text("\n".join(sorted(lines, key=lambda line: line[66:])) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "prism"])
    parser.add_argument("--bootstrap")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    else:
        if not args.bootstrap:
            parser.error("prism requires --bootstrap")
        prism(args.bootstrap)
