#!/usr/bin/env bash
set -euo pipefail

# Defense in depth: this script can never target stable tags or branches.
[[ "$GITHUB_REF" == refs/heads/dev ]]
[[ "$TAG" == "dev-$GITHUB_RUN_ID" && "$GITHUB_RUN_ID" =~ ^[1-9][0-9]*$ ]]
[[ "$REUSED" == true || "$REUSED" == false ]]
if [[ "$REUSED" == false ]]; then
  git config user.name 'github-actions[bot]'
  git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
  git add pack.toml index.toml
  git commit -m "chore: build $TAG"
  git tag "$TAG"
  git push origin "refs/tags/$TAG"
else
  git diff --exit-code -- pack.toml index.toml
fi

# Distinguish a missing release from an API/network error.
releases=$(gh api --paginate "repos/$GH_REPO/releases" --jq '.[].tag_name')
if ! grep -Fxq "$TAG" <<< "$releases"; then
  notes="$RUNNER_TEMP/dev-release-notes.md"
  cat > "$notes" <<EOF
Build de développement issu de dev au commit $GITHUB_SHA.

- Client auto-actualisé : importer Rocher-Suchard-DEV-Prism.zip dans Prism (Java 21).
- Client figé sur ce build : importer le fichier .mrpack versionné.
- Serveur de test : https://raw.githubusercontent.com/$GH_REPO/refs/heads/dev-latest/pack.toml
- Source figée : https://raw.githubusercontent.com/$GH_REPO/refs/tags/$TAG/pack.toml

Le canal dev-latest avance après publication si ce commit est toujours en tête de dev.
Les téléchargements Latest et le serveur stable restent sur main.
EOF
  gh release create "$TAG" --draft --verify-tag --prerelease --latest=false \
    --title "Rocher Suchard DEV $GITHUB_RUN_ID (${GITHUB_SHA:0:7})" --notes-file "$notes"
fi
if [[ $(gh release view "$TAG" --json isDraft --jq .isDraft) == true ]]; then
  assets=(dist/SHA256SUMS.txt)
  while IFS= read -r line; do
    assets+=("dist/${line:66}")
  done < dist/SHA256SUMS.txt
  gh release upload "$TAG" "${assets[@]}" --clobber
  gh release edit "$TAG" --draft=false --prerelease --latest=false
fi
# A retry must not promote a manually altered or incorrectly published release.
[[ $(gh release view "$TAG" --json isPrerelease --jq .isPrerelease) == true ]]

# An old build/retry must not roll the development installation endpoint back.
remote_dev=$(git ls-remote --exit-code origin refs/heads/dev | cut -f1)
if [[ "$remote_dev" != "$GITHUB_SHA" ]]; then
  echo "A newer dev commit exists; leaving dev-latest unchanged."
  exit 0
fi
old=$(git ls-remote origin refs/heads/dev-latest | cut -f1)
git push --force-with-lease="refs/heads/dev-latest:$old" origin "$TAG:refs/heads/dev-latest"
