# Serveur local Packwiz

Ce dossier démarre un serveur NeoForge 1.21.1 local à partir des sources
Packwiz du dépôt. Le service `packwiz` sert le contenu courant du dépôt ; le
service `minecraft` emploie le programme d'installation Packwiz de l'image
`itzg/minecraft-server` et télécharge uniquement les mods applicables au
serveur.

Le monde, les logs, les mods téléchargés et la configuration générée sont
conservés dans `deploy/data/`. Ce répertoire est ignoré par Git.

Docker Desktop doit être démarré avant d'exécuter les commandes ci-dessous.

## Démarrer

Depuis la racine du dépôt :

```sh
make refresh
docker compose -f deploy/compose.yaml up --build
```

Le premier démarrage télécharge NeoForge et les mods. Une fois que la console
indique que le serveur est prêt, connectez le client à `localhost:25565`.

Pour suivre seulement les journaux du serveur :

```sh
docker compose -f deploy/compose.yaml logs -f minecraft
```

Arrêtez proprement le serveur avec `Ctrl+C`, puis :

```sh
docker compose -f deploy/compose.yaml down
```

## Tester une modification du pack

1. Modifiez les métadonnées ou les fichiers de configuration.
2. Lancez `make refresh`.
3. Relancez `docker compose -f deploy/compose.yaml up --build`.

Pour un test entièrement neuf, arrêtez les services, puis supprimez
`deploy/data/` avant de relancer Compose. Cette suppression efface aussi le
monde local de test.

## Compatibilité testée

Le conteneur ne reçoit que les mods dont `side` vaut `server` ou `both` dans
les fichiers `mods/*.pw.toml`. Les ajouts client-only ne sont donc pas chargés
par le serveur. Cela permet de vérifier les deux chemins de compatibilité : un
client Prism d'origine sur le serveur optimisé, et le client optimisé sur ce
serveur ou sur l'ancien serveur.

`MEMORY` est réglé à 4 Go pour le test local. Ajustez cette valeur dans
`compose.yaml` si la machine hôte le nécessite.
