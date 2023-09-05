#Uno.py
#UTF-8

import discord
import random

client = discord.Client()

# Liste des joueurs
joueurs = []
# Cartes en main de chaque joueur
mains = {}
# Pioche
pioche = []
# Carte en jeu
carte_en_jeu = None

# Règles du jeu
regles = {
    "zero_echange": False,
    "double": False
}

# Emojis pour représenter les cartes
emojis = {
    "0": ":zero:",
    "1": ":one:",
    "2": ":two:",
    "3": ":three:",
    "4": ":four:",
    "5": ":five:",
    "6": ":six:",
    "7": ":seven:",
    "8": ":eight:",
    "9": ":nine:",
    "skip": ":no_entry_sign:",
    "reverse": ":arrow_backward:",
    "draw_two": ":1234:",
    "wild": ":large_blue_diamond:",
    "wild_draw_four": ":large_orange_diamond:"
}

# Création de la pioche et mélange
for couleur in ["red", "yellow", "green", "blue"]:
    for valeur in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        pioche.append((couleur, valeur))
    for special in ["skip", "reverse", "draw_two"]:
        pioche.append((couleur, special))
for wild in ["wild", "wild_draw_four"]:
    for i in range(4):
        pioche.append((wild, wild))
random.shuffle(pioche)

# Fonction pour distribuer les cartes aux joueurs
def distribuer():
    for joueur in joueurs:
        main = []
        for i in range(7):
            carte = pioche.pop()
            main.append(carte)
        mains[joueur] = main

# Fonction pour afficher les cartes en main d'un joueur
def afficher_main(joueur):
    main = mains[joueur]
    message = "Voici votre main :\n"
    for carte in main:
        couleur, valeur = carte
        emoji = emojis[valeur]
        message += f"{emoji} "
    return message

# Commande pour ajouter un joueur
@client.command(name="join")
async def join(ctx):
    # Vérifier si le joueur n'est pas déjà dans la liste
    if ctx.author in joueurs:
        await ctx.send("Vous êtes déjà dans la partie.")
        return
    # Ajouter le joueur à la liste et envoyer un message de confirmation
    joueurs.append(ctx.author)
    await ctx.send("Vous avez rejoint la partie.")

# Commande pour ajouter un ordinateur
@client.command(name="add_ai")
async def add_ai(ctx):
    # Ajouter un ordinateur à la liste
    joueurs.append("AI")
    await ctx.send("Un ordinateur a été ajouté à la partie.")

# Commande pour activer/désactiver une règle
@client.command(name="set_rule")
async def set_rule(ctx, rule: str, value: bool):
    # Vérifier que la règle existe
    if rule not in regles:
        await ctx.send("Cette règle n'existe pas.")
        return
    # Modifier la valeur de la règle
    regles[rule] = value
    if value:
        await ctx.send(f"La règle '{rule}' a été activée.")
    else:
        await ctx.send(f"La règle '{rule}' a été désactivée.")

# Commande pour lancer la partie
@client.command(name="start")
async def start(ctx):
    # Vérifier qu'il y a au moins deux joueurs
    if len(joueurs) < 2:
        await ctx.send("Il n'y a pas assez de joueurs pour démarrer la partie.")
        return
    # Distribuer les cartes aux joueurs
    distribuer()
    # Afficher les cartes en main de chaque joueur
    for joueur in joueurs:
        if joueur == "AI":
            continue
        message = afficher_main(joueur)
        await joueur.send(message)
    # Piocher une carte pour mettre en jeu
    global carte_en_jeu
    carte_en_jeu = pioche.pop()
    couleur, valeur = carte_en_jeu
    emoji = emojis[valeur]
    await ctx.send(f"La carte en jeu est {emoji}.")

# Commande pour jouer une carte
@client.command(name="play")
async def play(ctx, index: int):
    # Vérifier que c'est au tour du joueur
    if ctx.author != joueurs[0]:
        await ctx.send("Ce n'est pas votre tour.")
        return
    # Vérifier que l'index de la carte est valide
    main = mains[ctx.author]
    if index < 0 or index >= len(main):
        await ctx.send("Index de carte invalide.")
        return
    # Récupérer la carte jouée et la retirer de la main du joueur
    carte = main.pop(index)
    couleur, valeur = carte
    emoji = emojis[valeur]
    # Vérifier si la carte peut être jouée
    couleur_en_jeu, valeur_en_jeu = carte_en_jeu
    if couleur != couleur_en_jeu and valeur != valeur_en_jeu:
        await ctx.send("Vous ne pouvez pas jouer cette carte.")
        return
    # Mettre la carte en jeu
    carte_en_jeu = carte
	 # Appliquer les effets de la carte
	if valeur == "skip":
		joueurs.rotate(-1)
	elif valeur == "reverse":
		joueurs.reverse()
	elif valeur == "draw_two":
		next_player = joueurs[1]
		main = mains[next_player]
		for i in range(2):
			carte = pioche.pop()
			main.append(carte)
		joueurs.rotate(-1)
	elif valeur == "wild":
		couleur = None
		while couleur not in ["red", "yellow", "green", "blue"]:
			message = "Choisissez une couleur (red, yellow, green, blue) :"
			await ctx.send(message)
			# Attendre la réponse du joueur
			def check(m):
				return m.author == ctx.author and m.channel == ctx.channel
			try:
				message = await client.wait_for("message", check=check, timeout=60.0)
			except asyncio.TimeoutError:
				await ctx.send("Temps écoulé.")
				return
			couleur = message.content.lower()
		carte_en_jeu = (couleur, valeur)
	elif valeur == "wild_draw_four":
		couleur = None
		while couleur not in ["red", "yellow", "green", "blue"]:
			message = "Choisissez une couleur (red, yellow, green, blue) :"
			await ctx.send(message)
			# Attendre la réponse du joueur
			def check(m):
				return m.author == ctx.author and m.channel == ctx.channel
			try:
				message = await client.wait_for("message", check=check, timeout=60.0)
			except asyncio.TimeoutError:
				await ctx.send("Temps écoulé.")
				return
			couleur = message.content.lower()
		carte_en_jeu = (couleur, valeur)
		next_player = joueurs[1]
		main = mains[next_player]
		for i in range(4):
			carte = pioche.pop()
			main.append(carte)
		joueurs.rotate(-1)
	else:
		joueurs.rotate(-1)
	# Envoyer un message de confirmation
	await ctx.send(f"{ctx.author.mention} a joué la carte {emoji}.")
	# Vérifier si le joueur a gagné
	if len(main) == 0:
		await ctx.send(f"{ctx.author.mention} a gagné la partie !")
		# Réinitialiser la partie
		joueurs.clear()
		mains.clear()
		pioche.clear()
		return
	# Si c'est au tour d'un ordinateur, jouer automatiquement
	if joueurs[0] == "AI":
		couleur_en_jeu, valeur_en_jeu = carte_en_jeu
		joue = False
		# Vérifier si l'ordinateur peut jouer une carte de la même couleur
		for i, carte in enumerate(main):
			couleur, valeur = carte
			if couleur == couleur_en_jeu:
				main.pop(i)
				carte_en_jeu = carte
				joue = True
				break
		# Sinon, vérifier si l'ordinateur peut jouer une carte de la même valeur
		if not joue:
			for i, carte in enumerate(main):
				couleur, valeur = carte
				if valeur == valeur_en_jeu:
					main.pop(i)
					carte_en_jeu = carte
					joue = True
					break
		# Si l'ordinateur ne peut pas jouer, piocher une carte
		if not joue:
			carte = pioche.pop()
			main.append(carte)
		else:
			couleur, valeur = carte
			emoji = emojis[valeur]
			await ctx.send(f"L'ordinateur a joué la carte {emoji}.")
		# Vérifier si l'ordinateur a gagné
		if len(main) == 0:
			await ctx.send("L'ordinateur a gagné la partie !")
			# Réinitialiser la partie
			joueurs.clear()
			mains.clear()
			pioche.clear()
			return
		# Si c'est au tour d'un ordinateur, jouer automatiquement
		if joueurs[0] == "AI":
			couleur_en_jeu, valeur_en_jeu = carte_en_jeu
			joue = False
			# Vérifier si l'ordinateur peut jouer une carte de la même couleur
			for i, carte in enumerate(main):
				couleur, valeur = carte
				if couleur == couleur_en_jeu:
					main.pop(i)
					carte_en_jeu = carte
					joue = True
					break
			# Sinon, vérifier si l'ordinateur peut jouer une carte de la même valeur
			if not joue:
				for i, carte in enumerate(main):
					couleur, valeur = carte
					if valeur == valeur_en_jeu:
						main.pop(i)
						carte_en_jeu = carte
						joue = True
						break
		# Si l'ordinateur ne peut pas jouer, piocher une carte
		if not joue:
			carte = pioche.pop()
			main.append(carte)
		else:
			couleur, valeur = carte
			emoji = emojis[valeur]
			await ctx.send(f"L'ordinateur a joué la carte {emoji}.")
		# Vérifier si l'ordinateur a gagné
		if len(main) == 0:
			await ctx.send("L'ordinateur a gagné la partie !")
			# Réinitialiser la partie
			joueurs.clear()
			mains.clear()
			pioche.clear()
			return
		
# ----------- #
		
# Commande pour ajouter un joueur
@client.command(name="join")
async def join(ctx):
    # Vérifier que la partie n'a pas déjà commencé
    if len(joueurs) > 0:
        await ctx.send("La partie a déjà commencé.")
        return
    # Vérifier que le joueur n'est pas déjà dans la partie
    if ctx.author in joueurs:
        await ctx.send("Vous êtes déjà dans la partie.")
        return
    # Ajouter le joueur à la liste
    joueurs.append(ctx.author)
    await ctx.send(f"{ctx.author.mention} a rejoint la partie.")

# Commande pour ajouter un joueur ordinateur
@client.command(name="join_ai")
async def join_ai(ctx):
    # Vérifier que la partie n'a pas déjà commencé
    if len(joueurs) > 0:
        await ctx.send("La partie a déjà commencé.")
        return
    # Vérifier que le joueur ordinateur n'est pas déjà dans la partie
    if "AI" in joueurs:
        await ctx.send("Le joueur ordinateur est déjà dans la partie.")
        return
    # Ajouter le joueur ordinateur à la liste
    joueurs.append("AI")
    await ctx.send("Le joueur ordinateur a rejoint la partie.")

# Commande pour commencer la partie
@client.command(name="start")
async def start(ctx):
    # Vérifier qu'il y a au moins deux joueurs
    if len(joueurs) < 2:
        await ctx.send("Il faut au moins deux joueurs pour démarrer la partie.")
        return
    # Initialiser les mains des joueurs
    for joueur in joueurs:
        main = []
        for i in range(7):
            carte = pioche.pop()
            main.append(carte)
        mains[joueur] = main
    # Mélanger la pioche
    random.shuffle(pioche)
    # Prendre une carte au hasard pour déterminer la carte en jeu
    carte_en_jeu = pioche.pop()
    # Envoyer les mains des joueurs et la carte en jeu
    for joueur in joueurs:
        main = mains[joueur]
        message = f"Voici votre main :\n"
        for carte in main:
            couleur, valeur = carte
            emoji = emojis[valeur]
            message += f"{emoji} "
        await ctx.send(message)
    couleur, valeur = carte_en_jeu
    emoji = emojis[valeur]
    await ctx.send(f"La carte en jeu est {emoji}.")
# Commande pour jouer une carte
@client.command(name="play")
async def play(ctx, *, valeur):
    # Vérifier que la partie a démarré
    if ctx.author not in joueurs:
        await ctx.send("La partie n'a pas encore commencé ou vous n'êtes pas dans la partie.")
        return
    # Vérifier que c'est au tour du joueur
    if ctx.author != joueurs[0]:
        await ctx.send("Ce n'est pas votre tour.")
        return
    # Récupérer la main du joueur
    main = mains[ctx.author]
	# Vérifier si le joueur a une carte de la valeur jouée
	a_joue = False
	for i, carte in enumerate(main):
		couleur, valeur_carte = carte
		if valeur_carte == valeur:
			main.pop(i)
			carte_en_jeu = carte
			a_joue = True
			break
	if not a_joue:
		await ctx.send("Vous n'avez pas de carte de cette valeur.")
		return
# Commande pour afficher sa main
@client.command(name="main")
async def main(ctx):
    if ctx.author not in joueurs:
        await ctx.send("La partie n'a pas encore commencé ou vous n'êtes pas dans la partie.")
        return
    main = mains[ctx.author]
    if not main:
        await ctx.send("Vous n'avez plus de cartes.")
        return
    message = f"Votre main :\n"
    for carte in main:
        couleur, valeur = carte
        emoji = emojis[valeur]
        message += f"{emoji} "
    await ctx.author.send(message)


# Appliquer les effets de la carte
def switch(valeur):
    switcher = {
        "skip": skip,
        "reverse": reverse,
        "draw_two": draw_two,
        "wild": wild,
    }
    return switcher.get(valeur, "invalid")

def skip():
    # Passer au joueur suivant
    joueurs.rotate(-1)

def reverse():
    # Inverser l'ordre des joueurs
    joueurs.reverse()

def draw_two():
    # Faire piocher deux cartes au joueur suivant
    joueur_suivant = joueurs[1]
    main_suivante = mains[joueur_suivant]
    for i in range(2):
        carte = pioche.pop()
        main_suivante.append(carte)
    mains[joueur_suivant] = main_suivante
    # Passer au joueur suivant
    joueurs.rotate(-1)

def wild():
    # Demander au joueur de choisir une couleur
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content in ["red", "yellow", "green", "blue"]
    await ctx.send("Choisissez une couleur : red, yellow, green, blue")
    try:
        message = await client.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé.")
        return
    couleur_choisie = message.content
    # Appliquer la couleur choisie à la carte en jeu
    couleur_en_jeu, valeur_en_jeu = carte_en_jeu
    couleur_en_jeu = couleur_choisie
    carte_en_jeu = (couleur_en_jeu, valeur_en_jeu)

switch(valeur)()



