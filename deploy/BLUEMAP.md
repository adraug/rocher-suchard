# BlueMap et Create BlueMap

## Versions et perimetre

- BlueMap **5.7-neoforge** : projet Modrinth `swbUV1cr`, version `8iJcPOHJ`.
- Create BlueMap **1.1.1** : projet Modrinth `W9e7rf1y`, version `B1EqQDIC`.
- Les deux manifestes Packwiz sont `side = "server"`. Rien a installer sur les clients pour rejoindre le serveur ou consulter la carte dans un navigateur.
- Minecraft 1.21.1, NeoForge 21.1.251 et Create 6.0.10 restent inchanges. Aucun changement de recettes ou de progression.

BlueMap produit une carte web 3D. Create BlueMap ajoute l'affichage des trains et, selon sa configuration, du reseau ferroviaire. Ce n'est pas une integration generaliste de toutes les machines Create ni une garantie de rendu des contraptions Aeronautics.

## Premiere activation sur le serveur de test

1. Installer le pack contenant cet ajout avec Packwiz en mode serveur, puis demarrer le serveur pour generer les configurations.
2. Dans `config/bluemap/core.conf`, lire les commentaires de `accept-download`. Passer cette option a `true` uniquement apres avoir accepte les conditions indiquees et confirme la possession d'une licence Minecraft. Le pack ne prend pas cette decision pour l'administrateur.
3. Pour commencer, limiter explicitement le rendu dans ce meme fichier :

   ```hocon
   render-thread-count: 2
   ```

   C'est un point de depart prudent, pas une mesure de performance du serveur. Le premier rendu doit etre surveille : CPU, memoire, espace disque et MSPT/TPS. Eviter de le cumuler avec une grosse generation de chunks/Distant Horizons.
4. BlueMap preconfigure des cartes pour les mondes trouves. Examiner `config/bluemap/maps/` avant le premier rendu et ne conserver que les cartes necessaires au test.
5. Configurer le port HTTP dans `config/bluemap/webserver.conf` : `8100` est le port par defaut. Choisir un port effectivement disponible et alloue au serveur dans Calagopus.
6. Appliquer les changements avec `/bluemap reload`, puis suivre la progression avec `/bluemap` et les logs.

Pour privilegier les sessions de jeu, il est aussi possible de mettre `player-render-limit: 1` dans `config/bluemap/plugin.conf` : le rendu BlueMap est alors suspendu lorsqu'au moins un joueur est connecte. Cela ne constitue pas une garantie de charge nulle pour le mod ou ses addons.

## Calagopus / Traefik

L'ajout des mods ne cree ni allocation reseau, ni regle de pare-feu, ni route Traefik.

Allouer un port TCP supplementaire au conteneur Minecraft et faire correspondre le port d'ecoute BlueMap avec le port interne reel. Pour un acces via Traefik, cibler l'adresse et le port que Traefik peut effectivement joindre. Ne pas utiliser `127.0.0.1` comme backend entre deux conteneurs distincts. Aucune adresse, aucun domaine ni port de production n'est impose ici.

La carte peut exposer les constructions et les positions des joueurs. Decider de son audience avant toute publication ; si l'acces doit rester prive, restreindre aussi l'acces direct au port backend, pas seulement l'URL HTTPS du proxy.

## Create BlueMap

Sur un monde existant, verifier le fichier genere dans `<monde>/serverconfig/create_bluemap-server.toml`. Le mod enregistre une configuration NeoForge de type SERVER.

Garder `renderTracks = false` au premier essai : l'auteur signale un risque de lag avec l'affichage des lignes sur les grands reseaux. Valider d'abord l'affichage d'un train existant et ses mises a jour. Activer ensuite les voies seulement apres avoir mesure la charge. Ne pas reduire agressivement les intervalles de mise a jour.

Les fichiers de configuration generes restent locaux et ne sont pas geres par Packwiz dans cet ajout. Les prochains changements du pack ne doivent donc pas ecraser le consentement au telechargement, les ports, les cartes ou les choix de rendu de l'administrateur.

## Validation avant fusion / production

- Demarrage du serveur dedie avec les deux nouveaux JAR, sans erreur de dependance.
- Connexion avec les clients existants, sans les deux nouveaux mods cote client, notamment Prism et Mac.
- Premiere activation, rendu limite de la base et ouverture de la carte web.
- Verification des blocs moddes, des trains, des marqueurs et du comportement apres redemarrage/rechargement BlueMap.
- Comparaison CPU, memoire, disque et MSPT/TPS avant/apres ; surveiller particulierement le premier rendu et l'activation des voies.

Les controles des manifestes et de l'export ne remplacent pas ces essais en jeu. Aucun deploiement sur le serveur de production n'est effectue par cette PR.

## Sources

- https://modrinth.com/plugin/bluemap/version/5.7-neoforge
- https://modrinth.com/mod/create-bluemap/version/1.1.1
- https://modrinth.com/mod/create-bluemap
- https://bluemap.bluecolored.de/wiki/getting-started/Installation.html
- https://bluemap.bluecolored.de/wiki/configs/Core.html
- https://bluemap.bluecolored.de/wiki/configs/Plugin.html
- https://bluemap.bluecolored.de/wiki/configs/Webserver.html
- https://github.com/Szedann/create-bluemap/blob/afa50eeb71e597f728ba3c66371b375bad262358/src/main/java/dev/szedann/create_bluemap/Config.java
- https://github.com/Szedann/create-bluemap/blob/afa50eeb71e597f728ba3c66371b375bad262358/src/main/java/dev/szedann/create_bluemap/Create_bluemap.java

Les pages du wiki BlueMap evoluent avec les versions recentes : pour cet ajout, privilegier les commentaires des configurations effectivement generees par **5.7** si une option differe.
