# Tester le dernier développement

Le canal stable reste réservé à `main` : release GitHub **Latest** et source
Packwiz `latest`. Le canal `dev-latest` suit le dernier build publié avec succès
du dernier commit de `dev`. Une publication n'est pas une validation en jeu.

## Première activation

Après fusion du workflow dans `dev`, le push déclenche automatiquement
**Release development modpack**. Attendre sa réussite et la publication de la
prérelease `dev-<identifiant du run>` avant de configurer les installations.
L'URL `dev-latest` n'existe pas avant cette première publication.

Chaque prérelease possède un tag immuable, un `.mrpack`, une archive Packwiz,
un egg, les checksums et `Rocher-Suchard-DEV-Prism.zip`. Les tags `dev-*` ne
participent pas au calcul des versions stables. Les versions de développement
reprennent la version source de `pack.toml`, suivie de `-dev.<run>.g<commit>`.

La commande manuelle `workflow_dispatch` n'est proposée par GitHub que lorsque
le workflow existe aussi dans la branche par défaut. D'ici là, utiliser le
push sur `dev` ou **Re-run jobs** sur un run existant. Une relance réutilise son
tag ; une ancienne relance ne peut pas faire reculer `dev-latest`.

## Serveur de test Calagopus

1. Créer un **nouveau serveur**, avec son propre monde et son propre port.
2. Importer/utiliser l'egg habituel, avec Java 21.
3. Mettre **Packwiz URL** sur :

   ```text
   https://raw.githubusercontent.com/adraug/rocher-suchard/refs/heads/dev-latest/pack.toml
   ```

4. Utiliser Minecraft 1.21.1 et NeoForge 21.1.251 pour le pack actuel.
5. Démarrer le serveur. Après un nouveau build DEV réussi, le redémarrer pour
   synchroniser les mods et configurations.

Ne pas remplacer l'URL du serveur des joueurs : elle reste sur `latest`.
Si une future mise à jour change NeoForge, ajuster aussi la variable NeoForge
du serveur avant de le redémarrer.

## Serveur de test local avec Docker

Docker doit être démarré. Depuis le dépôt :

```sh
docker compose -f deploy/compose.dev.yaml up -d
docker compose -f deploy/compose.dev.yaml logs -f minecraft
```

Se connecter à `localhost:25566`. Cette configuration utilise le canal publié,
sans construire les sources locales. Son monde est dans `deploy/data-dev/`,
séparé du monde de `compose.yaml` et du serveur stable. Le port est accessible
uniquement depuis cet ordinateur.

Pour récupérer le prochain build réussi :

```sh
docker compose -f deploy/compose.dev.yaml restart minecraft
```

## Client Prism auto-actualisé

1. Ouvrir les [releases](https://github.com/adraug/rocher-suchard/releases) et
   choisir la prérelease du dernier build DEV réussi.
2. Télécharger **Rocher-Suchard-DEV-Prism.zip**.
3. Dans Prism : **Ajouter une instance → Importer depuis un ZIP**.
4. Utiliser Java 21 et lancer **Rocher Suchard DEV**. L'instance réserve jusqu'à
   6 Go de RAM ; ajuster si nécessaire.

L'archive contient Minecraft/NeoForge déclarés et le bootstrap Packwiz officiel.
Elle télécharge les mods au premier lancement, puis les actualise avant chaque
lancement. Garder cette instance séparée du client stable. Si Prism demande de
valider les commandes personnalisées lors de l'import, autoriser la commande
Packwiz fournie pour activer les mises à jour.

Si les versions Minecraft/NeoForge changent, accepter la proposition de mise à
jour de Packwiz et relancer l'instance si nécessaire, ou réimporter l'archive
Prism du nouveau build.

Une erreur de synchronisation doit être corrigée avant de jouer ; ne pas
contourner le pré-lancement en lançant un ancien client sur un serveur actualisé.

## Aligner client et serveur / revenir à un build précis

Un nouveau build peut sortir entre le redémarrage du serveur et le lancement du
client. Pour une session reproductible, utiliser le même tag `dev-<run>` :

- Serveur : remplacer `refs/heads/dev-latest` dans l'URL par
  `refs/tags/dev-<run>`.
- Client simple : importer le `.mrpack` versionné de cette prérelease dans une
  **autre instance**, qui ne suit pas automatiquement les mises à jour.
- Client Prism auto-actualisé : modifier l'URL dans **Paramètres → Commandes
  personnalisées → Pré-lancement**, en conservant le reste de la commande.
- Docker : définir `DEV_PACKWIZ_URL` sur l'URL figée avant `docker compose -f
  deploy/compose.dev.yaml up -d` (un simple restart ne change pas l'environnement).

Le tag représente aussi la version exacte des configurations. Pour revenir au
suivi continu, remettre l'URL `refs/heads/dev-latest/pack.toml` des deux côtés.

## Isolation de la publication

Le workflow de développement ne pousse ni `main`, ni `dev`, ni `latest`, ni les
tags stables `v*`. Il crée une prérelease explicitement marquée
`--prerelease --latest=false`. L'alias Packwiz `dev-latest` n'avance qu'après
publication complète des fichiers. Un build échoué laisse l'ancien alias en
place. Un build devenu obsolète peut rester disponible par son tag, mais ne
remplace pas l'alias.

Sources : [Packwiz Installer](https://packwiz.infra.link/tutorials/installing/packwiz-installer/),
[commandes Prism](https://prismlauncher.org/wiki/help-pages/custom-commands/).
