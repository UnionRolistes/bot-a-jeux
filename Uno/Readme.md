UNO sur Discord

UNO est un jeu de cartes où les joueurs doivent essayer de se débarrasser de toutes leurs cartes en les plaçant sur un tas en respectant certaines règles. Ce projet consiste en un bot Discord qui permet aux utilisateurs de jouer à UNO sur leur serveur.
Prérequis

    Python 3.7 ou supérieur
    Un token d'application Discord
    Un serveur Discord

Installation

    Clonez le dépôt :

git clone https://github.com/<your-username>/uno-discord.git

    Installez les dépendances :

pip install -r requirements.txt

    Créez un fichier .env et ajoutez votre token d'application Discord :

echo DISCORD_TOKEN=your-token > .env

    Modifiez le prefixe d'utilisation du bot dans le fichier bot.py (par défaut, il est défini sur .) :

client = commands.Bot(command_prefix='.')

    Exécutez le bot :

python bot.py

Utilisation

Voici la liste des commandes disponibles pour jouer à UNO sur Discord :

    .join : Rejoindre la partie
    .start : Commencer
