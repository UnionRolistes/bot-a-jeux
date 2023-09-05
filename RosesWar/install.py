#!/bin/bash

# Demander le token du bot Discord
echo -n "Entrez le token du bot Discord : "
read token

# Demander le prefixe à utiliser sur Discord
echo -n "Entrez le prefixe à utiliser sur Discord : "
read prefix

# Créer le fichier de configuration config.ini
echo "token = $token" > config.ini
echo "prefix = $prefix" >> config.ini

# Installer les dépendances avec pip
pip install -r requirements.txt

# Lancer le bot
python main.py
