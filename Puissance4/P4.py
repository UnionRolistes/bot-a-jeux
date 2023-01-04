import random
import discord

from discord.ext import commands

client = commands.Bot(command_prefix = '.')

scores = {}  # Dictionnaire pour stocker les scores

#def afficher_grille(grille):
#    # Afficher la première ligne
#    print("  1 2 3 4 5 6 7")
#    print(" ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐")
#    
#    # Afficher chaque ligne de la grille
#    for i, ligne in enumerate(grille):
#        # Afficher le numéro de la ligne
#        print(f"{i+1} ", end="")
#        # Afficher chaque colonne de la ligne
#        for j, case in enumerate(ligne):
#            # Afficher le caractère de la case
#            if case == "X":
#                print("X", end=" ")
#            elif case == "O":
#                print("O", end=" ")
#            else:
#                print(" ", end=" ")
#            # Afficher la séparation entre les colonnes
#            if j < len(ligne) - 1:
#                print("│", end=" ")
#        # Afficher la séparation entre les lignes
#        if i < len(grille) - 1:
#            print("\n ├──┼───┼───┼───┼───┼───┼───")
#        else:
#            print("\n └──────┴──────┴──────┴──────┴──────┴──────┴──────┘")



@client.command()
async def puissance4(ctx):
  # Créer la grille de jeu
  grille = [[' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ']]

  # Dictionnaire pour associer chaque joueur à un emoji
  joueurs = {'joueur 1': ':red_circle:', 'joueur 2': ':large_blue_circle:'}

  # Déterminer qui commence
  tour = random.choice(list(joueurs.keys()))

  # Envoyer un message indiquant qui commence
  await ctx.send(f'{tour} commence!')

  while True:
    # Afficher la grille de jeu
    message = '\n'
    for ligne in grille:
      for colonne in ligne:
        message += f' {colonne} '
      message += '\n'
    await ctx.send(message)

    # Demander au joueur de jouer
    await ctx.send(f'{tour}, où voulez-vous jouer?')

    # Attendre la réponse du joueur
    def check(m):
      return m.author == ctx.message.author and m.content.isdigit()
    try:
      move = int(await client.wait_for('message', check=check, timeout=30))
    except:
      await ctx.send('Temps écoulé!')
      return

    # Vérifier que le coup est valide
    if move < 0 or move > 6:
      await ctx.send('Coup non valide, veuillez réessayer.')
      continue
    if grille[move][5] != ' ':
      await ctx.send('Colonne pleine, veuillez réessayer.')
      continue

    # Jouer le coup
    for i in range(6):
      if grille[move][i] == ' ':
        grille[move][i] = joueurs[tour]
        break

    # Vérifier si le joueur a gagné
    if check_win(grille,
    def check_win(grille, symbol):
      # Vérifier les lignes
      for ligne in grille:
        for i in range(4):
          if ligne[i] == symbol and ligne[i+1] == symbol and ligne[i+2] == symbol and ligne[i+3] == symbol:
            return True

      # Vérifier les colonnes
      for i in range(7):
        for j in range(3):
          if grille[i][j] == symbol and grille[i][j+1] == symbol and grille[i][j+2] == symbol and grille[i][j+3] == symbol:
            return True

      # Vérifier les diagonales
      for i in range(4):
        for j in range(3):
          if grille[i][j] == symbol and grille[i+1][j+1] == symbol and grille[i+2][j+2] == symbol and grille[i+3][j+3] == symbol:
            return True
      for i in range(4):
        for j in range(3):
          if grille[i][j+3] == symbol and grille[i+1][j+2] == symbol and grille[i+2][j+1] == symbol and grille[i+3][j] == symbol:
            return True

      return False

    def check_full(grille):
      for ligne in grille:
        for colonne in ligne:
          if colonne == ' ':
            return False
      return True

    @client.command()
    async def top(ctx):
      # Trier le dictionnaire "scores" par valeur
      scores_triés = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}

      # Afficher le top 10
      message = '```\n'  # Ouvrir une zone de texte en utilisant les "backticks"
      message += 'Classement des meilleurs joueurs:\n'
      message += '-------------------------------\n'
      for i, (joueur, score) in enumerate(scores_triés.items()):
        date = score['date'].strftime('%d/%m/%Y %H:%M:%S')  # Formater la date au format "dd/mm/yyyy hh:mm:ss"
        message += f'{i+1}. {joueur}: {score["points"]} points (joué le {date})\n'
        if i == 9:
          break
      message += '```'  # Fermer la zone de texte
      await ctx.send(message)

    client.run('TOKEN')


