# Rocher Suchard

Rocher Suchard is a NeoForge modpack for Minecraft 1.21.1. This repository is
the Packwiz source of the pack; it is the reference from which the distributable
Modrinth archive is built.

## Release policy

Version 1.0 is the original pack shared by friends, imported from Prism Launcher.
Version 1.1 is the current content update, including the additional mods tracked
in this repository. Test client/server compatibility before publishing a release.

## Requirements

- Minecraft 1.21.1
- NeoForge 21.1.251
- [Packwiz](https://packwiz.infra.link/), available on `PATH`
- GNU Make, available by default on macOS developer environments

The Makefile accepts a different Packwiz path when needed:

```sh
make PACKWIZ=/path/to/packwiz export
```

## Repository layout

| Path | Purpose |
| --- | --- |
| `pack.toml` | Pack identity, version, Minecraft and NeoForge versions. |
| `index.toml` | Generated inventory and hashes of the pack files. |
| `mods/*.pw.toml` | Packwiz metadata for downloadable mods. |
| `config/` | Client and server configuration reproduced from Prism. |
| `.packwizignore` | Repository files excluded from Minecraft exports. |
| `dist/` | Generated Modrinth archives; ignored by Git. |

## Configuration

Keep the configuration inherited from the original Prism pack to preserve its
settings. Machine-specific files such as `config/sodium-fingerprint.json` are
excluded from Git and Packwiz exports and may be regenerated locally by mods.

## Daily workflow

Edit `pack.toml`, a mod metadata file, or a configuration file, then refresh
the Packwiz index and inspect the result:

```sh
make refresh
make status
```

Build the distributable archive with:

```sh
make export
```

This always refreshes `index.toml` first and writes
`dist/Rocher Suchard-<version>.mrpack`. Generated archives are intentionally
not committed: commit the Packwiz source files instead.

Other commands:

```sh
make clean    # remove generated archives
make pull     # fast-forward from the Git remote
make push     # push the current branch
```

`make pull` and `make push` require a configured upstream remote. The current
checkout does not have one, so configure it before using those targets.

## Local server test

The [deploy/README.md](deploy/README.md) instructions start a local NeoForge
server with Docker Compose directly from this Packwiz source. The environment
installs server-only and shared mods only, so it can validate compatibility
with both the original Prism client and the optimized client.

## Calagopus deployment

The [egg/README.md](egg/README.md) guide contains a Calagopus/Pterodactyl egg
for a NeoForge server synchronized from a Packwiz `pack.toml` URL. It installs
the NeoForge version declared by the egg, then applies Packwiz server-side
updates on every server start.

## Before a release

1. Run `make export` and install the `.mrpack` in a fresh launcher profile.
2. Join the target server and verify client/server compatibility.
3. Merge the pull request into `main` to publish automatically.

The `Release modpack` GitHub Action runs after each pull request merged into
`main`, including squash and rebase merges. Closing an unmerged pull request or
pushing directly does not publish a release. It increments the patch version
(`1.1` → `1.1.1` → `1.1.2`), runs `make export`, and publishes a GitHub release
with the `.mrpack`, `SHA256SUMS.txt`, source archives, and GitHub-generated
release notes listing merged pull requests and contributors.

The version is stored in `pack.toml` in the release tag and exported archive.
`main` retains the base version; future versions are allocated from the highest
version among existing `vX.Y.Z` tags and `pack.toml`. Increase the base version
manually to start a new minor/major series. Release commits are attached to the
exact merged commit, without pushing generated commits back to `main`.

Releases run serially (up to 100 pending runs). Re-run a failed Actions run to
resume its existing tag/draft; published releases are not overwritten. The
workflow uses the built-in `GITHUB_TOKEN` with `contents: write`; no custom
secret is needed. Repository rules must allow this token to create `v*` tags.
Client/server testing remains a prerequisite before merging content changes.

## Pack maintenance

Use Packwiz to add, update, pin, or remove mods. Do not edit generated hashes
in `index.toml` by hand; `make refresh` derives them from the source files.
Keep the Packwiz metadata, configuration, and generated index together in each
commit so another maintainer can reproduce the exact archive.
