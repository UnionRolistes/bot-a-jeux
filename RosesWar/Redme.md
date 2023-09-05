# La Guerre des Roses

Application de jeu de cartes en ligne pour Discord utilisant l'API Discord.py.

## Description
Le "Jeux des roses" est un jeu de cartes qui a été publié par Alderac Entertainment Group en 2005. 

Le jeu se base sur le même scénario que le jeu de rôle grandeur nature du même nom, à savoir la Guerre des Roses qui a eu lieu en Angleterre au 15ème siècle.

Dans le "Jeux des roses" (version cartes), les joueurs incarnent les leaders de l'une des deux factions en lice (Lancaster ou York) et doivent affronter leurs adversaires en utilisant des unités militaires et des cartes spéciales qui ont des effets spéciaux. 

Le but du jeu est de capturer ou de détruire les unités ennemies ou de prendre le contrôle de territoires clés.

Le "Jeux des roses" (version cartes) est un jeu de stratégie et de bluff qui demande aux joueurs de prévoir les actions de leurs adversaires et de réagir en conséquence. 

Le jeu est composé de plusieurs extensions qui ajoutent de nouvelles cartes et de nouvelles mécaniques de jeu. Il est possible de jouer en solo ou en multijoueur.

## Prérequis

    Un serveur Discord
    Un bot Discord avec un token d'authentification

## Installation

    Cloner le dépôt Github sur votre ordinateur
    Ouvrir un terminal et se rendre dans le répertoire du dépôt cloné
    Exécuter la commande pip install -r requirements.txt pour installer les dépendances nécessaires
    Modifier le fichier config.py avec votre token de bot et le préfixe de commande souhaité
    Exécuter le fichier main.py

## Utilisation

    Inviter le bot sur votre serveur Discord
    Créer une chaîne de commande et utiliser les commandes suivantes pour jouer :
        !join pour ajouter un joueur
        !start pour commencer la partie
        !play <carte> pour jouer une carte de votre main
        !rules pour afficher les règles du jeu

## Commandes custome

Il est possible d'ajouter des règles personnalisées en modifiant le fichier custom_rules.py.

## Licence

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.

## Remerciements

    Discord.py
    Emojis ASCII Art
