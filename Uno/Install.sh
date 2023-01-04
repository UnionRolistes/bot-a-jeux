#!/bin/bash

echo "Bienvenue dans l'installateur de UNO sur Discord !"

echo "Entrez votre token d'application Discord :"
read token
echo "Entrez le prefixe à utiliser sur Discord :"
read prefix

# Création du fichier .env
echo "DISCORD_TOKEN=$token" > .env
echo "DISCORD_PREFIX=$prefix" >> .env

echo "Installation des dépendances..."
pip install -r requirements.txt

echo "Installation terminée !"
echo "Pour démarrer l'application, exécutez 'python bot.py'"
