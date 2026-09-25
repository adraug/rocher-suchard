"""Assemble a self-hostable Packwiz source and checksums for release assets."""

import hashlib
import json
from pathlib import Path
import shutil
import tomllib
import zipfile


def prepare():
    root = Path.cwd()
    dist = root / "dist"
    pack = tomllib.loads((root / "pack.toml").read_text())
    index_path = root / pack["index"]["file"]
    index = tomllib.loads(index_path.read_text())
    digest = hashlib.new(pack["index"]["hash-format"], index_path.read_bytes()).hexdigest()
    if digest != pack["index"]["hash"]:
        raise ValueError("Packwiz index hash mismatch; run make refresh")

    mrpack = dist / f'{pack["name"]}-{pack["version"]}.mrpack'
    if not mrpack.is_file():
        raise FileNotFoundError(f"Missing export: {mrpack}")
    with zipfile.ZipFile(mrpack) as archive:
        manifest = json.loads(archive.read("modrinth.index.json"))
        if manifest["versionId"] != pack["version"] or manifest["dependencies"] != pack["versions"]:
            raise ValueError("Export version or loaders do not match pack.toml")

    files = {root / "pack.toml", index_path}
    for entry in index["files"]:
        path = (index_path.parent / entry["file"]).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f"Invalid Packwiz path: {entry['file']}")
        digest = hashlib.new(entry.get("hash-format", index["hash-format"]), path.read_bytes()).hexdigest()
        if digest != entry["hash"]:
            raise ValueError(f"Packwiz hash mismatch: {entry['file']}")
        files.add(path)

    source = dist / f'Rocher-Suchard-{pack["version"]}-packwiz.zip'
    with zipfile.ZipFile(source, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            # Stable timestamps make retries produce identical source archives.
            info = zipfile.ZipInfo(path.relative_to(root).as_posix(), (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())

    # GitHub rewrites spaces in uploaded names; checksum the exact published name.
    published_mrpack = dist / f'Rocher-Suchard-{pack["version"]}.mrpack'
    stable_mrpack = dist / "Rocher-Suchard.mrpack"
    shutil.copyfile(mrpack, published_mrpack)
    shutil.copyfile(mrpack, stable_mrpack)
    assets = [published_mrpack, stable_mrpack, source]
    for path in [root / "pack.toml", index_path, root / "egg/egg-rocher-suchard-packwiz-neoforge.json"]:
        target = dist / path.name
        shutil.copyfile(path, target)
        assets.append(target)
    (dist / "SHA256SUMS.txt").write_text("".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
        for path in sorted(assets)
    ))
    print(f"Prepared {len(assets)} assets and SHA256SUMS.txt")


if __name__ == "__main__":
    prepare()
