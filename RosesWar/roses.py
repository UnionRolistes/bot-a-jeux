#roses.py
#UTF-8
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="!")

# Dictionnaire des joueurs et de leur main
joueurs = {}

# Dictionnaire des territoires et de leur propriétaire
territoires = {}

# Dictionnaire des effets des cartes spéciales
effets = {}

# Charger les cartes spéciales et leurs effets à partir d'un fichier ou d'une base de données

# Fonction pour distribuer les cartes aux joueurs au début de la partie
def distribuer_cartes():
    # Mélanger les cartes
    # Répartir les cartes aux joueurs
    # Enregistrer les mains des joueurs dans le dictionnaire joueurs

# Commande pour afficher la main du joueur
@client.command(name="main")
async def main(ctx):
    # Récupérer la main du joueur à partir du dictionnaire joueurs
    main = joueurs[ctx.author]
    # Envoyer la main du joueur en message privé
    await ctx.author.send("Voici votre main :")
    for carte in main:
        await ctx.author.send(f"- {carte.nom} ({carte.valeur} points)")

# Commande pour jouer une carte
@client.command(name="jouer")
async def jouer(ctx, carte: str):
    # Récupérer la main du joueur à partir du dictionnaire joueurs
    main = joueurs[ctx.author]
    # Trouver la carte dans la main du joueur
    for i, c in enumerate(main):
        if c.nom.lower() == carte.lower():
            # Supprimer la carte de la main du joueur
            del main[i]
            # Appliquer l'effet de la carte
            effet = effets[c.effet]
            effet(ctx.author, ctx.channel)
            # Enregistrer la nouvelle main du joueur dans le dictionnaire joueurs
            joueurs[ctx.author] = main
            break
    else:
        await ctx.send("Vous ne possédez pas cette carte.")

# Fonction pour appliquer les effets de la carte
def effet(joueurs, territoires, canal, carte):
    # Appliquer l'effet de la carte en fonction de son nom ou de sa valeur
    if carte.nom == "Conquête":
        # Demander à l'utilisateur quel territoire conquérir
        # Conquérir le territoire
        pass
    elif carte.nom == "Destruction":
        # Demander à l'utilisateur quelle unité détruire
        # Détruire l'unité
        pass
    # ...


# Fonction pour capturer un territoire
#def capturer(joueur, canal, territoire):
    # Vérifier si le territoire est déjà occupé
    # Modifier le propriétaire du territoire dans le dictionnaire territoires
    # Envoyer un message dans le canal pour informer des changements de propriété
# Fonction pour conquérir un territoire
def conquete(joueurs, territoires, canal, carte):
    # Demander à l'utilisateur quel territoire conquérir
    message = await canal.send("Quel territoire voulez-vous conquérir?")
    # Attendre la réponse de l'utilisateur
    reponse = await client.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
    # Vérifier si le territoire est valide et disponible
    if reponse.content in territoires and territoires[reponse.content] is None:
        # Conquérir le territoire
        territoires[reponse.content] = ctx.author
        await canal.send(f"{ctx.author.mention} a conquis le territoire de {reponse.content}!")
    else:
        await canal.send("Territoire invalide ou déjà conquis.")

# Fonction pour détruire une unité
def destruction(joueurs, territoires, canal, carte):
    # Demander à l'utilisateur quelle unité détruire
    message = await canal.send("Quelle unité voulez-vous détruire?")
    # Attendre la réponse de l'utilisateur
    reponse = await client.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
    # Vérifier si l'unité existe et appartient à un joueur adverse
    if reponse.content in territoires and territoires[reponse.content] != ctx.author:
        # Détruire l'unité
        territoires[reponse.content] = None
        await canal.send(f"{ctx.author.mention} a détruit l'unité de {reponse.content}!")
    else:
        await canal.send("Unité invalide ou appartenant à votre équipe.")

# Fonction pour vérifier si un joueur a gagné
def verifier_victoire(joueur):
    # Vérifier si le joueur a conquis tous les territoires
    if all(territoire == joueur for territoire in territoires.values()):
        return True
    # Vérifier si le joueur a détruit toutes les unités ennemies
    ennemies = [territoire for territoire in territoires.values() if territoire is not None and territoire != joueur]
    if not ennemies:
        return True
    return False
    
    

# Fonction pour détruire une unité
def detruire(joueur, canal, unité):
    # Chercher l'unité à détruire dans les mains des autres joueurs
    for autre_joueur, main in joueurs.items():
        if autre_joueur == joueur:
            continue
        for i, carte in enumerate(main):
            if carte.nom.lower() == unité.lower():
                # Supprimer l'unité de la main du joueur
                del main[i]
                # Enregistrer la nouvelle main du joueur dans le dictionnaire joueurs
                joueurs[autre_joueur] = main
                # Envoyer un message dans le canal pour informer de la destruction de l'unité
                await canal.send(f"{joueur.mention} a détruit l'unité {carte.nom} de {autre_joueur.mention} !")
                return
    await canal.send("Aucune unité de ce nom n'a été trouvée.")

# Fonction pour afficher l'état actuel des territoires
@client.command(name="territoires")
async def territoires(ctx):
    # Construire le message à envoyer en parcourant le dictionnaire territoires
    message = "Voici l'état actuel des territoires :\n"
    for t, j in territoires.items():
        message += f"- {t}: occupé par {j.mention}\n"
    await ctx.send(message)

# Fonction pour vérifier si un joueur a gagné
def verifier_victoire(joueur):
    # Vérifier si le joueur a conquis tous les territoires ou détruit toutes les unités ennemies
    pass

# Boucle de jeu principale
while True:
    # Pour chaque joueur dans l'ordre défini par le dictionnaire joueurs
        # Afficher la main du joueur
        # Demander à quelle carte jouer
        # Jouer la carte
        # Vérifier si le joueur a gagné
    # Passer au joueur suivant

# Fonction pour afficher le classement des joueurs
@client.command(name="classement")
async def classement(ctx):
    # Construire le message à envoyer en triant les joueurs par points
    message = "Voici le classement des joueurs :\n"
    joueurs_triés = sorted(joueurs.items(), key=lambda x: x[1].points, reverse=True)
    for joueur, score in joueurs_triés:
        message += f"- {joueur.mention}: {score.points} points\n"
    await ctx.send(message)

# Lancer le bot
client.run("TOKEN")

