# Egg Calagopus : Rocher Suchard

[`egg-rocher-suchard-packwiz-neoforge.json`](egg-rocher-suchard-packwiz-neoforge.json)
est un egg au format Pterodactyl (`PTDL_v2`), compatible avec Calagopus. Il
prépare un serveur Java 21, télécharge NeoForge puis exécute Packwiz avec le
côté `server` à chaque démarrage. Les mods `server` et `both` sont donc
installés, tandis que les mods `client` restent exclus.

La version NeoForge par défaut est `21.1.251`, identique à celle de
[`pack.toml`](../pack.toml).

## Préparer la source Packwiz

L'egg a besoin d'une URL HTTP(S), accessible depuis le nœud qui exécute le
serveur, et qui répond directement avec le `pack.toml` de ce dépôt. Par
exemple :

```text
https://raw.githubusercontent.com/adraug/rocher-suchard/latest/pack.toml
```

Cette URL suit la dernière release publiée. Pour figer la version, remplacez
`latest` par `v1.1.0` (ou le tag souhaité). Le prochain redémarrage applique
les mises à jour si vous suivez `latest` ; gardez clients et serveur sur la même
version du pack.

La release contient aussi l'egg, une archive `*-packwiz.zip` pour auto-héberger
la source complète, et `SHA256SUMS.txt`. L'URL GitHub
`/releases/latest/download/pack.toml` sert au téléchargement du fichier seul,
pas à l'installation : les sous-dossiers nécessaires n'y sont pas disponibles.

Cette source doit aussi exposer `index.toml`, les fichiers de configuration et
les métadonnées Packwiz référencés par l'index. Elle ne doit pas pointer vers
un fichier `.mrpack`.

Avant de publier une nouvelle version sur cette source, mettez l'index à jour :

```sh
make refresh
```

## Importer l'egg

1. Dans Calagopus, ouvrez l'administration puis le nest Minecraft.
2. Importez `egg-rocher-suchard-packwiz-neoforge.json` depuis un fichier.
3. Créez le serveur avec l'image **Java 21** proposée par l'egg et une
   allocation de port Minecraft.
4. Renseignez **Packwiz URL** avec l'URL directe du `pack.toml` publié.
5. Laissez **Version NeoForge** à `21.1.251`, sauf si `pack.toml` a été mis à
   jour vers une autre version.
6. Lancez le serveur. Au premier démarrage, NeoForge et les mods applicables
   au serveur sont téléchargés ; les démarrages suivants ne récupèrent que les
   différences détectées par Packwiz.

La commande de démarrage de l'egg appelle `bash start.sh`. La logique conditionnelle
NeoForge/Packwiz reste dans ce script afin d'éviter que l'entrypoint Pterodactyl
n'interprète prématurément les constructions shell (`if`, `then`, etc.).

L'egg écrit également `eula=true` et configure `server.properties` avec le
port attribué par le panel.

## Mémoire JVM par serveur

Les réglages de mémoire Java sont exposés comme variables éditables dans
Calagopus, indépendamment de la limite RAM du conteneur :

| Variable | Défaut | Valeurs admises |
| --- | --- | --- |
| `JVM_INITIAL_RAM_PERCENTAGE` | `25` | Entier de 1 à 90 |
| `JVM_MAX_RAM_PERCENTAGE` | `75` | Entier de 1 à 90 |

Le pourcentage initial doit être inférieur ou égal au maximum. Java calcule les
tailles du heap par rapport à la mémoire disponible pour la JVM (normalement la
limite mémoire du conteneur Docker avec Java 21). Avec un serveur limité à
16 Gio, les valeurs par défaut donnent environ 4 Gio au démarrage et 12 Gio
maximum, tout en réservant une marge pour la mémoire hors heap. Le script
refuse les valeurs invalides avant l'installation/synchronisation des mods.

Le fichier `user_jvm_args.txt` reste chargé : s'il contient des options de
heap actives (`-Xms`, `-Xmx`, `-XX:InitialRAMPercentage`,
`-XX:MaxRAMPercentage`), celles-ci peuvent prendre le dessus sur les variables
de l'egg. Le script affiche alors un avertissement ; supprimez ces options du
fichier pour piloter la mémoire uniquement depuis Calagopus. Les lignes
commentées du fichier ne déclenchent pas l'avertissement.

**Serveurs déjà installés :** l'import d'un egg mis à jour ne régénère pas
automatiquement leur fichier `start.sh`, créé pendant l'installation de
l'egg. Après import, vérifiez la présence des nouvelles variables dans le
panel, puis mettez à jour `start.sh` sur chaque serveur existant (ou
réexécutez l'installation uniquement après sauvegarde complète et vérification
de ses effets). Une simple synchronisation Packwiz ne modifie pas ce script.

## Mettre le serveur à jour

1. Commitez et publiez les sources Packwiz, y compris `pack.toml` et
   `index.toml` mis à jour.
2. Redémarrez le serveur dans Calagopus.
3. Packwiz compare l'index et applique les fichiers serveur nécessaires avant
   le lancement de NeoForge.

Si la version NeoForge de `pack.toml` change, modifiez aussi **Version
NeoForge** dans Calagopus puis redémarrez. L'egg télécharge et installe la
version demandée avant la synchronisation Packwiz.

La version 1.0 correspond au pack Prism initial partagé entre amis ; la
version 1.1 ajoute du contenu. Utilisez des clients et un serveur avec la même
version du pack et vérifiez leur compatibilité avant publication.

## Canal de développement

Pour suivre `dev-latest` sur un serveur séparé et une instance Prism dédiée,
consulter le [guide DEV](../deploy/DEV.md). Le serveur stable conserve son URL
`latest`.
