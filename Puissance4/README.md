Puissance 4 en ASCII

Ce projet consiste en un jeu de puissance 4 en ASCII jouable via l'API Discord.
Prérequis

Pour jouer à ce jeu, vous avez besoin :

    d'un compte Discord
    d'un serveur Discord où vous pouvez inviter des bot
    d'un token de bot Discord (obtenu en créant un bot sur le site de développement de Discord)

Installation

    Clonez ce dépôt sur votre ordinateur : git clone https://github.com/<votre_nom_d'utilisateur>/puissance4-ascii.git
    Ouvrez le fichier config.py et entrez votre token de bot dans la variable TOKEN
    Définissez le prefix de commande de votre choix dans la variable PREFIX (par exemple, .)
    Installez les dépendances nécessaires en exécutant la commande pip install -r requirements.txt
    Invitez le bot sur votre serveur Discord en utilisant l'URL suivante : https://discord.com/api/oauth2/authorize?client_id=<votre_id_de_client>&permissions=0&scope=bot

Utilisation

Une fois le bot installé sur votre serveur Discord, vous pouvez utiliser les commandes suivantes :

    .puissance4 : lance une partie de puissance 4
    .top : affiche le classement des 10 meilleurs joueurs
    .help : affiche l'aide avec la liste des commandes disponibles

Pour jouer à la partie de puissance 4, utilisez les réactions de la partie (🔴 ou ⚪) pour placer votre jeton.
Contribuer

Si vous souhaitez contribuer à ce projet, n'hésitez pas à ouvrir une pull request avec vos modifications. Toute contribution est la bienvenue !
