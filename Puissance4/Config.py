#install.sh
#utf-8
#!/bin/bash

# Demander l'URL du dépôt à cloner
read -p "Entrez l'URL du dépôt à cloner: " repo_url

# Cloner le dépôt
git clone $repo_url

# Demander le jeton Discord
read -p "Entrez votre jeton Discord: " token

# Demander le préfixe d'utilisation
read -p "Entrez le préfixe d'utilisation: " prefix

# Écrire le jeton et le préfixe dans le fichier de configuration
echo "TOKEN=$token" > .env
echo "PREFIX=$prefix" >> .env

# Installer les dépendances
pip install -r requirements.txt

# Exécuter le script
python main.py
