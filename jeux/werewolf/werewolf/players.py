import random

class Roles:
    '''énumère les rôles proposés'''
    villager = "villager"
    werewolf = "werewolf"
    witch = "witch"
    psychic = "psychic"

def how_many_werewolfs(players_count, hard=False):
    '''algorithme de détermination du nombre de loups-garous par rapport au nombre de joueurs'''
    if hard:
        if players_count < 12:
            return 3
        if players_count < 18:
            return 4
        return 5
    else:
        if players_count < 12:
            return 2
        if players_count < 18:
            return 3
        return 4

def put_a_psychic(players_count, werewolves_count, hard=False):
    '''Décide si une voyante doit être ajoutée au jeu'''
    return True

def put_a_witch(players_count, werewolves_count, hard=False):
    '''Décide si une sorcière doit être ajoutée au jeu'''
    # TODO: choix d'algo complètement arbritraire, à revoir
    if hard:
        return True
    if players_count < werewolves_count + 12:
        return True
    return True

def make_stack(players_count, hard=False):
    '''Création de la pile mélangée de rôles qui vont être distribués'''

    stack = [Roles.villager] * players_count
    werewolves_count = how_many_werewolfs(players_count, hard)

    # On crée une liste des id de stack car on va la dépiler aléatoirement après
    indexes = list(range(players_count))

    secure_random = random.SystemRandom()

    # Désignation random des loups-garou
    for i in range(werewolves_count):
        position = secure_random.choice(indexes)
        indexes.remove(position)
        stack[position] = Roles.werewolf

    # Désignation random de la voyante (si voyante il doit y avoir)
    if put_a_psychic(players_count, werewolves_count, hard):
        position = secure_random.choice(indexes)
        indexes.remove(position)
        stack[position] = Roles.psychic

    # Désignation random de la sorcière (si sorcière il doit y avoir)
    if put_a_witch(players_count, werewolves_count, hard):
        position = secure_random.choice(indexes)
        indexes.remove(position)
        stack[position] = Roles.witch

    return stack

class Players:
    '''Classe (un peu bordélique) qui gère les joueurs, leurs rôles, leurs états'''

    def __init__(self):
        # Catalagogue des joueurs, il est indexé par leurs id et chaque entrée est elle même un dictionnaire
        # qui permet de définir le rôle du joueur, son état (vivant ou mort), ses posessions pour les
        # rôle particuliers (la sorcière et ses potions par ex)
        self.__players = {}

        # Dictionnaire référençant les joueurs par rôle, il est donc indexé par le rôle (voir la
        # classe Roles au dessus) et chaque entrée est une liste des joueurs correspondant à ce rôle
        self.__roles = {}

        # Mémorise qui a gagné quand cela a été détecté
        self.winner = None

        # Mémorise le dernier joueur tué
        self.last_dead = None

    def add_player(self, id):
        if id in self.__players:
            return False
        self.__players[id] = {"role": "", "alive": True}
        return True

    def role_distribution(self):
        stack = make_stack(len(self.__players))

        # attribution des rôle aux joueurs en dépilant les cartes
        for id, player in self.__players.items():
            role = stack.pop() #rappel: pop() enlève l'élément de la liste

            if role not in self.__roles:
                self.__roles[role] = []
            self.__roles[role].append(id)
            player["role"] = role

            #cas particulier de la sorcière
            if role ==  Roles.witch:
                player["potions"] = ["heal","poison"]
            #cas particulier de la sorcière
            if role ==  Roles.psychic:
                player["last vision"] = None

    def get_role(self, id):
        return self.__players[id]["role"]

    def get_all_ids(self):
        return self.__players.keys()

    def get_werewolves_ids(self):
        return self.__roles[Roles.werewolf].copy()

    def get_psychic_id(self):
        return self.__roles[Roles.psychic][0]

    def get_witch_id(self):
        return self.__roles[Roles.witch][0]

    def get_werewolves_ids_but(self, id):
        l = self.__roles[Roles.werewolf].copy()
        l.remove(id)
        return l

    def is_a_werewolf(self, id):
        return self.__players[id]["role"] == Roles.werewolf

    def is_alive(self, id):
        return self.__players[id]["alive"]

    def seek_role(self, role):
        return role in self.__roles

    def turn_to_dead(self, id):
        self.last_dead = id
        self.__players[id]["alive"] = False

    def werewolves_living(self):
        return [id for id in self.__roles[Roles.werewolf] if self.is_alive(id)]

    def villagers_living(self):
        return [id for id in self.__players if self.is_alive(id) and not self.is_a_werewolf(id)]

    def players_living(self):
        return [id for id in self.__players if self.is_alive(id)]

    def psychic_choice(self, target):
        self.__players[self.__roles[Roles.psychic][0]]["last vision"] = target

    def psychic_vision(self):
        vision = self.__players[self.__roles[Roles.psychic][0]]["last vision"]
        self.__players[self.__roles[Roles.psychic][0]]["last vision"] = None
        if vision:
            return self.__players[vision]["role"]
        else:
            return None

    def game_is_over(self):
        if len(self.werewolves_living()) == 0:
            self.winner = Roles.villager
            return True
        elif len(self.villagers_living()) < 2:
            self.winner = Roles.werewolf
            return True
        elif len(self.villagers_living()) <= len(self.werewolves_living()) + 1:
            # TODO: à vérifier (notament s'il y a une sorcière avec au moins une potion)
            self.winner = Roles.werewolf
            return True
        else:
            return False
