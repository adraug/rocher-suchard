# Repository Guidelines

## Project Structure & Module Organization

This repository is the Packwiz source for the Rocher Suchard NeoForge modpack.
`pack.toml` defines the pack identity and Minecraft/NeoForge versions;
`index.toml` is the generated inventory. Keep mod metadata in
`mods/<mod-name>.pw.toml`. Preserve upstream configuration filenames under
`config/`, `defaultconfigs/`, `resourcepacks/`, and `shaderpacks/` because mods
may load them by exact path. `deploy/` contains the local Docker Compose server
test, and `egg/` contains the Calagopus/Pterodactyl server egg. Generated
Modrinth archives belong in ignored `dist/`.

## Build, Test, and Development Commands

- `make refresh` rebuilds `index.toml` after any pack, mod, or configuration
  change. Do this before reviewing or committing Packwiz content.
- `make export` refreshes the index and creates `dist/Rocher Suchard-<version>.mrpack`.
- `make status` shows pending Git changes; `make pull` uses fast-forward-only
  updates and `make push` publishes the tracked branch.
- `docker compose -f deploy/compose.yaml up --build` starts a local NeoForge
  server. Connect to `localhost:25565`; use `logs -f minecraft` to inspect it.
- Validate egg changes with `jq -e . egg/egg-rocher-suchard-packwiz-neoforge.json`.

Override Packwiz when needed: `make PACKWIZ=/path/to/packwiz refresh`.

## Content, Style, and Compatibility

Use Packwiz commands to add or update mods; do not hand-edit generated hashes
in `index.toml`. Follow existing lowercase, hyphenated `.pw.toml` names.
Preserve indentation and key order in TOML, JSON, JSON5, and properties files
unless a tool rewrites them. Mark mod sides accurately (`client`, `server`, or
`both`) so Packwiz installs the correct files on each environment.

Version 1.0 is the original Prism pack shared by friends. Version 1.1 is the
current content update. Test client/server compatibility before releasing
content changes; compatibility with the original pack must not be assumed.

## Testing and Review

There is no unit-test suite. For meaningful changes, run `make refresh`, build
an export when the client is affected, and test the relevant local server path.
Check both original Prism and optimized clients when changing shared or server
content. Do not commit `deploy/data/` or `dist/`.

## Commits and Pull Requests

Use concise imperative commits, preferably `type: summary` (for example,
`feat: add server-side optimization metadata`). Include Packwiz metadata,
configuration, and the regenerated index in one change. Pull requests should
state the Minecraft/NeoForge impact, mod-side impact, commands run, and the
client/server combinations tested.
