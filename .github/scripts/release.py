"""Allocate a patch version, or reuse the release tag for this merge on retry."""

import os
from pathlib import Path
import re
import subprocess
import tomllib


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def version(value):
    if not re.fullmatch(r"\d+\.\d+(?:\.\d+)?", value):
        raise ValueError(f"Unsupported release version: {value}")
    parts = tuple(map(int, value.split(".")))
    return parts if len(parts) == 3 else (*parts, 0)


def prepare():
    source = git("rev-parse", "HEAD")
    tags = sorted(
        (tag for tag in git("tag", "--list", "v*").splitlines()
         if re.fullmatch(r"v\d+\.\d+(?:\.\d+)?", tag)),
        key=lambda tag: version(tag[1:]),
    )
    reused = next(
        (tag for tag in tags
         if git("show", "-s", "--format=%P", tag) == source
         and git("show", "-s", "--format=%s", tag) == f"chore: release {tag}"),
        None,
    )
    if reused:
        tag = reused
        git("checkout", "--detach", tag)
    else:
        path = Path("pack.toml")
        content = path.read_text()
        base = version(tomllib.loads(content)["version"])
        latest = max((version(t[1:]) for t in tags), default=None)
        if latest is None or base > latest:
            major, minor, patch = base
        else:
            major, minor, patch = latest
            patch += 1
        value = f"{major}.{minor}.{patch}"
        tag = f"v{value}"
        content, count = re.subn(r'^version = "[^"]+"$', f'version = "{value}"', content, count=1, flags=re.M)
        if count != 1:
            raise ValueError("Missing top-level version in pack.toml")
        path.write_text(content)
    previous = [t for t in tags if version(t[1:]) < version(tag[1:])]
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        output.write(f"tag={tag}\nprevious_tag={previous[-1] if previous else ''}\nreused={str(bool(reused)).lower()}\n")
    print(f"Release: {tag} (reused: {bool(reused)})")


if __name__ == "__main__":
    prepare()
