@client.command(name="help")
async def help(ctx, *args):
    # Si aucun argument n'est fourni, afficher la liste des commandes
    if not args:
        # Envoyer un message privé au joueur avec la liste des commandes
        await ctx.author.send("""
Voici la liste des commandes disponibles :

- `join` : Rejoindre la partie en cours ou en créer une nouvelle.
- `start` : Commencer la partie.
- `play <carte>` : Jouer une carte de votre main.
- `main` : Afficher votre main.
- `addai` : Ajouter un joueur ordinateur à la partie.
- `rmaai` : Supprimer un joueur ordinateur de la partie.
- `addrule <règle>` : Ajouter une règle custome à la partie.
- `rmrule <règle>` : Supprimer une règle custome de la partie.

Exemple : `!play 2` pour jouer la carte de valeur 2 de votre main.

Pour obtenir de l'aide sur les règles du jeu, utilisez la commande `!help rules`.
""")
    # Si l'argument "rules" est fourni, afficher les règles du jeu
    elif args[0] == "rules":
        # Envoyer un message privé au joueur avec les règles du jeu
        await ctx.author.send("""
Voici les règles du jeu :

1. Chaque joueur possède un deck de 40 cartes, divisé en quatre types : soldats, chevaliers, canons et généraux.
2. Le but du jeu est de conquérir tous les territoires ou de détruire toutes les unités ennemies.
3. Le tour d'un joueur consiste à jouer une carte de sa main et à utiliser son effet.
4. Les cartes peuvent être utilisées pour attaquer, défendre ou conquérir des territoires.
5. Lorsqu'un joueur perd toutes ses unités ou tous ses territoires, il est éliminé de la partie.
6. Le dernier joueur en jeu remporte la partie.

Voici les effets des différents types de cartes :

- Soldats : Peuvent attaquer ou défendre avec une force de 1.
- Chevaliers : Peuvent attaquer ou défendre avec une force de 2.
- Canons : Peuvent attaquer avec une force de 3, mais ne peuvent pas être utilisés pour défendre.
- Généraux : Peuvent attaquer ou défendre avec une force de 4.

Voici comment conquérir un territoire :

1. Jouez une carte de type "soldat" ou "chevalier" et utilisez son effet pour attaquer un territoire ennemi.
2. Si la force de votre attaque est supérieure à la défense du territoire, vous le conquérez.
3. Vous pouvez également conquérir un territoire en jouant une carte de type "général" et en utilisant son effet de conquête.

Voici comment détruire une unité :

1. Jouez une carte de type "canon" et utilisez son effet pour attaquer une unité ennemie.
2. Si la force de votre attaque est supérieure à la défense de l'unité, vous la détruisez.
3. Vous pouvez également détruire une unité en jouant une carte de type "général" et en utilisant son effet de destruction.
