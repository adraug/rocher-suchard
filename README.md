# Rocher Suchard

Rocher Suchard is a NeoForge modpack for Minecraft 1.21.1. This repository is
the Packwiz source of the pack; it is the reference from which the distributable
Modrinth archive is built.


## Installation du pack

La façon la plus simple d'installer la dernière version est d'utiliser l'archive
Modrinth publiée avec un nom stable :

**[Installer la dernière version de Rocher Suchard](https://github.com/adraug/rocher-suchard/releases/latest/download/Rocher-Suchard.mrpack)**

Cette URL suit toujours la dernière release GitHub publiée. Une archive versionnée
`Rocher-Suchard-<version>.mrpack` reste également disponible dans chaque release
pour conserver un lien immuable vers une version précise.

### Modrinth App

1. Cliquez sur **[Installer la dernière version](https://github.com/adraug/rocher-suchard/releases/latest/download/Rocher-Suchard.mrpack)**.
2. Ouvrez Modrinth App.
3. Importez le fichier `.mrpack` téléchargé comme nouveau profil/instance.
4. Lancez l'instance créée.

Le lien reste identique d'une release à l'autre : cliquer dessus récupère toujours
le dernier `.mrpack` publié. Modrinth App ne documente pas actuellement un import
direct depuis une URL externe équivalent à Prism ; une instance déjà importée
n'est donc pas mise à jour automatiquement par ce simple lien.

### Prism Launcher

Prism peut utiliser directement l'URL stable, sans téléchargement manuel :

1. Ouvrez **Add Instance** puis **Import**.
2. Collez cette URL dans le champ d'import :

   ```text
   https://github.com/adraug/rocher-suchard/releases/latest/download/Rocher-Suchard.mrpack
   ```

3. Validez l'import puis lancez l'instance.

Sur les versions récentes de Prism Launcher, un pack local peut également être
mis à jour depuis son URL source. L'URL reste donc la même lorsque Rocher Suchard
passe de `1.1.1` à `1.1.2`, `1.2.0`, etc.

Pour figer une version précise, utilisez à la place l'asset
`Rocher-Suchard-<version>.mrpack` de la release correspondante.

### Client manuel — pour les plus téméraires

Le pack peut aussi être installé sans importer le `.mrpack`, en partant d'une
instance Minecraft **1.21.1** avec **NeoForge 21.1.251**.

1. Installez Minecraft 1.21.1 et NeoForge 21.1.251.
2. Placez `packwiz-installer-bootstrap.jar` dans le dossier de l'instance.
3. Depuis ce dossier, synchronisez les fichiers client avec :

```sh
java -jar packwiz-installer-bootstrap.jar -g -s client \
  "https://raw.githubusercontent.com/adraug/rocher-suchard/latest/pack.toml"
```

4. Lancez ensuite le client NeoForge normalement.

Dans ce mode, relancer la commande Packwiz avant Minecraft permet de récupérer
les changements de la branche `latest`. C'est le mode le plus proche du
fonctionnement automatique utilisé côté serveur, mais il demande de gérer
vous-même le lancement de Packwiz et de NeoForge.

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

### Chunk loading

Chunk Loaders replaces FTB Chunks, FTB Teams, and FTB Library. Install the
updated pack on both clients and the server. Place a chunk loader, right-click
it, and select the chunks to keep loaded in its map. No teams or claims are
needed. Available tiers cover a single chunk or areas up to 3×3, 5×5, and 7×7.

Existing FTB forced chunks are not migrated: place loaders in the areas that
should remain active. Previous FTB claims no longer protect those areas.
Before release, check loading after disconnecting and restarting the server,
including a Create machine in a selected chunk. The original Prism client
must not be assumed compatible with this content change.

### Commands

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

Read the [1.1.0 changelog](changelogs/1.1.0.md) for additions and migration steps.
Version-specific notes in `changelogs/<version>.md` are included in the GitHub
release before the automatically generated list of pull requests and contributors.

1. Run `make export` and install the `.mrpack` in a fresh launcher profile.
2. Join the target server and verify client/server compatibility.
3. Merge the pull request into `main` to publish automatically.

The `Release modpack` GitHub Action runs after each pull request merged into
`main`, including squash and rebase merges. Closing an unmerged pull request or
pushing directly does not publish a release. The first release uses the base
version (`1.1` becomes `1.1.0`); subsequent merges increment the patch version
(`1.1.1`, `1.1.2`, ...). A higher base version starts a new series at that version.

Each release includes:

- `Rocher-Suchard-<version>.mrpack` for an immutable, versioned launcher download.
- `Rocher-Suchard.mrpack` as the stable alias used by
  `/releases/latest/download/Rocher-Suchard.mrpack`.
- `pack.toml` and `index.toml` for inspection or download.
- `Rocher-Suchard-<version>-packwiz.zip`, containing the complete Packwiz tree
  (pack, index, mod metadata, configurations and other indexed files), ready to
  extract at the root of an HTTP(S) server. Mod binaries are downloaded separately.
- `egg-rocher-suchard-packwiz-neoforge.json` for Calagopus/Pterodactyl.
- `SHA256SUMS.txt`, covering all six assets above. From the download directory,
  run `sha256sum -c SHA256SUMS.txt` (Linux) or `shasum -a 256 -c SHA256SUMS.txt`
  (macOS). GitHub's automatic source archives are not included in this manifest.
- GitHub-generated release notes listing merged pull requests and contributors.

For Calagopus, set **Packwiz URL** to the complete published source:

```text
https://raw.githubusercontent.com/adraug/rocher-suchard/latest/pack.toml
```

The `latest` branch points to the latest published release commit, including
all files needed by Packwiz. It is updated only after release assets are uploaded
and the release is public. To pin a server, replace `latest` with `v1.1.0` (or
another release tag). Keep NeoForge in the panel aligned with the selected pack.
Do not use `/releases/latest/download/pack.toml` as the installer URL: although
that URL downloads the file, release assets do not expose the required directory
structure for its relative references.

The version is stored in `pack.toml` in the release tag and exported archive.
`main` retains the base version; future versions are allocated from existing
`vX.Y.Z` tags and `pack.toml`. Release commits are attached to the exact merged
commit, without pushing generated commits back to `main`.

Releases run serially (up to 100 pending runs). Re-run a failed Actions run to
resume its existing tag/draft; published releases are not overwritten. The
workflow uses the built-in `GITHUB_TOKEN` with `contents: write`; no custom
secret is needed. Repository rules must allow this token to create `v*` tags
and update the generated `latest` branch, including non-fast-forward updates.
Client/server testing remains a prerequisite before merging content changes.

## Pack maintenance

Use Packwiz to add, update, pin, or remove mods. Do not edit generated hashes
in `index.toml` by hand; `make refresh` derives them from the source files.
Keep the Packwiz metadata, configuration, and generated index together in each
commit so another maintainer can reproduce the exact archive.
